
def main():
    error = EkpError.OK
    reader = None
    msg = u''
    try:
        import smartcard.System
        import smartcard.Session
    except ImportError as e:
        error = EkpError.ReadersNotConnected
        msg = u'(Бесконтактно) Не удалось импортировать модуль smartcard:\n {0}.'.format(e.message)
        logger.warning(msg)
        return error, msg

    readers = smartcard.System.readers()
    readers = filter(lambda x: x.name.lower().find('picc') != -1, readers)
    if not readers:
        error = EkpError.ReadersNotConnected
        msg = u'(Бесконтактно) Не найден бесконтактный считыватель.'
        logger.warning(msg)
    else:
        reader = readers[0]
        connection = reader.createConnection()
        connection.connect()
        SELECT = [0xff, 0xCA, 0x00, 0x00, 0x00]
        data, sw1, sw2 = connection.transmit(SELECT)
        res = int(str(hex(sw1)) + ('0' if len(str(hex(sw2))[2:]) < 2 else '') + str(hex(sw2))[2:], 16)
        bskNum = '0x'
        data = [hex(i) for i in data]
        for idx in reversed(xrange(len(data))):
            alignment = '0' if len(str(data[idx])[2:]) < 2 else ''
            bskNum += alignment + str(data[idx])[2:]


if __name__ == 'main':
    main()
