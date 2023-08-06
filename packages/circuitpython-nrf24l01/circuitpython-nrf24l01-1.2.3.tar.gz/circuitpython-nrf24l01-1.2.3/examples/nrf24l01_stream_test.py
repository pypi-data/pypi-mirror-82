"""
Example of library usage for streaming multiple payloads.
"""
import time
import board
import digitalio as dio
# if running this on a ATSAMD21 M0 based board
# from circuitpython_nrf24l01.rf24_lite import RF24
from circuitpython_nrf24l01.rf24 import RF24

# addresses needs to be in a buffer protocol object (bytearray)
address = b"1Node"

# change these (digital output) pins accordingly
ce = dio.DigitalInOut(board.D4)
csn = dio.DigitalInOut(board.D5)

# using board.SPI() automatically selects the MCU's
# available SPI pins, board.SCK, board.MOSI, board.MISO
spi = board.SPI()  # init spi bus object

# we'll be using the dynamic payload size feature (enabled by default)
# initialize the nRF24L01 on the spi bus object
nrf = RF24(spi, csn, ce)

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity
nrf.pa_level = -12


def make_buffers(size=32):
    """private function to construct a large list of payloads"""
    buffers = []
    # we'll use `size` for the number of payloads in the list and the
    # payloads' length
    for i in range(size):
        # prefix payload with a sequential letter to indicate which
        # payloads were lost (if any)
        buff = bytes([i + (65 if 0 <= i < 26 else 71)])
        for j in range(size - 1):
            char = bool(j >= (size - 1) / 2 + abs((size - 1) / 2 - i))
            char |= bool(j < (size - 1) / 2 - abs((size - 1) / 2 - i))
            buff += bytes([char + 48])
        buffers.append(buff)
        del buff
    return buffers


def master(count=1, size=32):  # count = 5 will transmit the list 5 times
    """Transmits multiple payloads using `RF24.send()` and `RF24.resend()`."""
    buffers = make_buffers(size)  # make a list of payloads
    nrf.open_tx_pipe(address)  # set address of RX node into a TX pipe
    nrf.listen = False  # ensures the nRF24L01 is in TX mode
    successful = 0  # keep track of success rate
    for _ in range(count):
        start_timer = time.monotonic() * 1000  # start timer
        # NOTE force_retry=2 internally invokes `RF24.resend()` 2 times at
        # most for payloads that fail to transmit.
        result = nrf.send(buffers, force_retry=2)  # result is a list
        end_timer = time.monotonic() * 1000  # end timer
        print("Transmission took", end_timer - start_timer, "ms")
        for r in result:  # tally the resulting success rate
            successful += 1 if r else 0
    print(
        "successfully sent {}% ({}/{})".format(
            successful / (size * count) * 100,
            successful,
            size * count
        )
    )


def master_fifo(count=1, size=32):
    """Similar to the `master()` above except this function uses the full
    TX FIFO and `RF24.write()` instead of `RF24.send()`"""
    if size < 6:
        print("setting size to 6;", size, "is not allowed for this test.")
        size = 6
    buf = make_buffers(size)  # make a list of payloads
    nrf.open_tx_pipe(address)  # set address of RX node into a TX pipe
    nrf.listen = False  # ensures the nRF24L01 is in TX mode
    for c in range(count):  # transmit the same payloads this many times
        nrf.flush_tx()  # clear the TX FIFO so we can use all 3 levels
        # NOTE the write_only parameter does not initiate sending
        buf_iter = 0  # iterator of payloads for the while loop
        failures = 0  # keep track of manual retries
        start_timer = time.monotonic() * 1000  # start timer
        while buf_iter < size:  # cycle through all the payloads
            while buf_iter < size and nrf.write(buf[buf_iter], write_only=1):
                # NOTE write() returns False if TX FIFO is already full
                buf_iter += 1  # increment iterator of payloads
            ce.value = True  # start tranmission (after 10 microseconds)
            while not nrf.fifo(True, True):  # updates irq_df flag
                if nrf.irq_df:
                    # reception failed; we need to reset the irq_rf flag
                    ce.value = False  # fall back to Standby-I mode
                    failures += 1  # increment manual retries
                    if failures > 99 and buf_iter < 7 and c < 2:
                        # we need to prevent an infinite loop
                        print(
                            "Make sure slave() node is listening."
                            " Quiting master_fifo()"
                        )
                        buf_iter = size + 1  # be sure to exit the while loop
                        nrf.flush_tx()  # discard all payloads in TX FIFO
                        break
                    nrf.clear_status_flags()  # clear the irq_df flag
                    ce.value = True  # start re-transmitting
            ce.value = False
        end_timer = time.monotonic() * 1000  # end timer
        print(
            "Transmission took {} ms with {} failures detected.".format(
                end_timer - start_timer,
                failures
            ),
            end=" " if failures < 100 else "\n"
        )
        if 1 <= failures < 100:
            print(
                "\n\nHINT: Try playing with the 'ard' and 'arc' attributes to"
                " reduce the number of\nfailures detected. Tests were better"
                " with these attributes at higher values, but\nnotice the "
                "transmission time differences."
            )
        elif not failures:
            print("You Win!")


def slave(timeout=5):
    """Stops listening after a `timeout` with no response"""
    # set address of TX node into an RX pipe. NOTE you MUST specify
    # which pipe number to use for RX, we'll be using pipe 0
    nrf.open_rx_pipe(0, address)  # pipe number options range [0,5]
    nrf.listen = True  # put radio into RX mode and power up
    count = 0  # keep track of the number of received payloads
    start_timer = time.monotonic()  # start timer
    while time.monotonic() < start_timer + timeout:
        if nrf.update() and nrf.pipe is not None:
            count += 1
            # retreive the received packet's payload
            rx = nrf.recv()  # clears flags & empties RX FIFO
            print("Received: {} - {}".format(rx, count))
            start_timer = time.monotonic()  # reset timer on every RX payload

    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode


print(
    """\
    nRF24L01 Stream test\n\
    Run slave() on receiver\n\
    Run master() on transmitter to use 1 level of the TX FIFO\n\
    Run master_fifo() on transmitter to use all 3 levels of the TX FIFO."""
)
