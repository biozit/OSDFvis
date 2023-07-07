class TransferTest:
  def __init__(self, source, sourceIP, destination, destinationIP, protocol, port, numTransfers):
    self.source = source
    self.destination = destination
    self.sourceIP = sourceIP
    self.destinationIP = destinationIP
    self.protocol = protocol
    self.port = port
    self.numTransfers = numTransfers
    self.rate = []
