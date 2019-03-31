from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream

DEFAULT_IP_ADDRESS = "127.0.0.1"
SIGNAL_NAMES = ['beta_relative']

class Player(object):
  """ defines the properties of a player """

  def __init__(self, port, ip_address=DEFAULT_IP_ADDRESS):
    self._ip_address = ip_address
    self._port = port
    self._is_playing = False
    self._signals = MuseOSCInputStream(SIGNAL_NAMES, ip_address, port)
    

  @property
  def ip_address(self):
    return self._ip_address

  @ip_address.setter
  def ip_address(self, ip_address):
    if not self._is_playing:
      self._ip_address = ip_address
      self._signals = MuseOSCInputStream(SIGNAL_NAMES, self._ip_address, self._port)
    else:
      raise Exception("The player is currently playing. Stop the game before setting params")
    
  @property 
  def port(self):
    return self._port

  @port.setter
  def port(self, port):
    if not self._is_playing:
      self._port = port
      self._signals = MuseOSCInputStream(SIGNAL_NAMES, self._ip_address, self._port)
    else: 
      raise Exception("The player is currently playing. Stop the game before setting params")
  
    
  def start(self):
    self._signals.start()
    self._is_playing = True

