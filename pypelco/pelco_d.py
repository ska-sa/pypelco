

class PelcoD(object):
    """Create PelcoD type messages."""

    RIGHT = 1
    LEFT = 0
    UP = 1
    DOWN = 0
    STOP = 3

    def __init__(self, address):
        self._address = int(address)
        self._word = [0, 0, 0, 0]
        self._pan_speed = 0x10
        self._tilt_speed = 0x10

    def __str__(self):
        return ''.join([chr(c) for c in self.msg_array()])

    def bin(self, separator=''):
        return str(separator).join(
            ['{0:08b}'.format(n) for n in self.msg_array()])

    def hex(self, separator=''):
        return str(separator).join(
            ['{0:02x}'.format(n) for n in self.msg_array()])

    def msg_array(self):
        """Return the message as a list.

        Returns
        -------

        List with 7 items.

        """
        msg = [255, self._address]
        msg.extend(self._word[0:4])
        msg.append(self.check_sum())
        return msg

    def check_sum(self):
        """Calculate the checksum of the message."""
        msg = [self._address]
        msg.extend(self._word[0:4])
        return sum(msg) & 255

    def set_word(self, word, value):
        """Set the value of word 3 to 6.

        Parameters
        ----------

        word: Integer
            Word [3-6] to set.

        value: Integer
            Value to set the word to. Must be from 0 to 255.

        """
        if word < 3 or word > 6:
            raise ValueError('Word out of range.')
        value = int(value) & 255  # Convert to 8 bit int.
        self._word[word - 3] = value

    def set_words(self, *args):
        """Set the value of the words."""
        for num, val in enumerate(args[0:4]):
            print('num ', num)
            print('val ', val)
            self.set_word(3 + num, val)

    def set_word_bit(self, word, bit, val):
        """Set or clear a bit on a word.

        Parameters
        ----------

        word: Integer
            Word [3-6] to set.

        bit: Integer
            Bit [0-7] to set.

        value: Boolean
            Value to set the word to. Must be True or False

        """
        if word < 3 or word > 6:
            raise ValueError('Word out of range.')

        if bit > 7:
            raise ValueError('Bit out of range.')

        pos = word - 3
        if val:
            # Set Bit
            self._word[pos] = self._word[pos] | (1 << bit)
        else:
            # Clear Bit
            self._word[pos] = self._word[pos] & ((1 << bit) ^ 255)

    def _send(self):
        if self._connection:
            self._connection.write(str(self.__str__))

    def _set_extended_commands(self, word4, w6_min, w6_max, value):
        value = int(value)
        if w6_max <= value <= w6_max:
            self.set_words(0x00, word4, 0x00, value)

    def command_extended(self, name, value=None):
        pass

    def _set_standard_command(self, word3_bits=None, word4_bits=None):
        if word3_bits is None:
            word3_bits = []
        elif not isinstance(word3_bits, list):
            word3_bits = [word3_bits]
        if word4_bits is None:
            word4_bits = []
        elif not isinstance(word4_bits, list):
            word4_bits = [word4_bits]

        word3 = 0
        for bit in word3_bits:
            word3 = word3 & (1 << bit)

        word4 = 0
        for bit in word4_bits:
            word4 = word4 & (1 << bit)
        self.set_words(word3, word4, self._pan_speed, self._tilt_speed)

    def camera_on(self):
        """Switch the camera on."""
        self._set_standard_command([7, 3])

    def camera_off(self):
        self._set_standard_command([3])

    def pan(self, direction, speed=None):
        """Pan the Camera.

        Parameters
        ----------

        direction: Int. One of LEFT, RIGHT, STOP
            Move the comera or stop it.

        speed: Optional. Integer. 0x00 - 0x3F, 0xFF
            The speed at wich the camera will move.
        """
        if direction == self.STOP:
            self.set_words(0, 0, 0, self._tilt_speed)
        elif direction == self.RIGHT:
            self._set_standard_command([], [1])
        elif direction == self.LEFT:
            self._set_standard_command([], [2])

    def tilt(self, direction, speed=None):
        pass

    @property
    def pan_speed(self, value):
        return self._pan_speed

    @pan_speed.setter
    def pan_speed(self, value):
        value = int(value)
        if value > 0x3F:
            value = 0xFF
        if value < 1:
            value = 1
        self._pan_speed = value

    @property
    def tilt_speed(self, value):
        return self._tilt_speed

    @tilt_speed.setter
    def tilt_speed(self, value):
        value = int(value)
        if value > 0x3F:
            value = 0x3F
        if value < 1:
            value = 1
        self._tilt_speed = value

    def up(self):
        self.tilt(self.UP, self._tilt_speed)

    def down(self):
        self.tilt(self.DOWN, self._tilt_speed)

    def right(self):
        self.pan(self.RIGHT, self._pan_speed)

    def left(self):
        self.pan(self.LEFT, self._pan_speed)

    def stop(self):
        self.set_words(0, 0, 0, 0)
#
