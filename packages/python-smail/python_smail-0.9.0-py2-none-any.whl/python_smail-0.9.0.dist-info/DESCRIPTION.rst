============
Python SMAIL
============

This library makes it simple to create S/MIME messages in Python. It supports signing (using RSA keys),
encryption (using a public RSA key, in AES128-CBC, AES192-CBC or AES256-CBC modes) and the combination of both -
where the message is first signed and the result is then encrypted (*"enveloped"*).

The foundation of python-smail is the `oscrypto`_ library which provides access to the C-bindings of OpenSSL
and implements many high and low level functionality. Additionally `asn1crypto`_ is used which is *"A fast, pure
Python library for parsing and serializing ASN.1 structures."*.


Requirements
------------

* Python 3.5+
* asn1crypto
* oscrypto


Example
-------

Encryption
##########

The code below loads Bob's public key in PEM format and uses it to encrypt
the e-mail in S/MIME format::

    import os
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from smail import encrypt_message

    message = MIMEText("This a plain text body!")
    message['Date'] = formatdate(localtime=True)
    message['From'] = "AliceRSA@example.com"
    message['To'] = "BobRSA@example.com"
    message['Subject'] = "Text Message - Encrypted"

    cert = os.path.join('tests', 'testdata', 'BobRSASignByCarl.pem')

    encrypted_message = encrypt_message(message, [cert])
    print(encrypted_message.as_string())

Output::

    MIME-Version: 1.0
    Content-Type: application/pkcs7-mime; smime-type=enveloped-data; name=smime.p7m
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename=smime.p7m
    Date: Tue, 17 Mar 2020 19:58:17 +0100
    From: AliceRSA@example.com
    To: BobRSA@example.com
    Subject: Plain Text Message

    MIIBhwYJKoZIhvcNAQcDoIIBeDCCAXQCAQAxgb4wgbsCAQAwJjASMRAwDgYDVQQD
    EwdDYXJsUlNBAhBGNGvHgABWvBHTbi7NXXHQMAsGCSqGSIb3DQEBAQSBgFmMsY5d
    H446eMYRwzVUREH2+Nv9VyflrA9rJlU/4yKqGGEnzt+YRPQaU+KoZ8iURaMB/GLE
    ZupCnJ79VAjs+RX6kyMtKMXvcsRkzR8GGGPLHNEbqqFmDY5VQrC/jA66w6/xPjdb
    hzVvf6SVWc4Aefv8xdQOMF1relsVahjvjFJrMIGtBgkqhkiG9w0BBwEwHQYJYIZI
    AWUDBAEqBBArK3YkdLMydTK8DyyQvUj+gIGAaC/h3NVeGcVpdkDI9iP4OxqC4chk
    BHeK+KpYJJYlelSt7D5LlRuRHjnRy3laU3bi1bxm0vxefx2ihf5rZRblpLWwnuft
    duFKvXKUX0Es6Q78LpY8Ng3IxMGYNMWiCTMyqDGgC32JRI3H8twsG0/NIoZxKDXQ
    1k7QedeP0a+JhVc=


Signing
#######

The code below loads Alice's private and public key in PEM format and uses it to
sign the e-mail in S/MIME format::

    import os
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from smail import sign_message

    message = MIMEText("This a plain text body!")
    message['Date'] = formatdate(localtime=True)
    message['From'] = "AliceRSA@example.com"
    message['To'] = "BobRSA@example.com"
    message['Subject'] = "Text Message - Signed"

    key_signer = os.path.join('tests', 'testdata', 'AlicePrivRSASign.pem')
    cert_signer = os.path.join('tests', 'testdata', 'AliceRSASignByCarl.pem')

    signed_message = sign_message(message, key_signer, cert_signer)
    print(signed_message.as_string())

Output::

    MIME-Version: 1.0
    Content-Type: multipart/signed; protocol="application/x-pkcs7-signature"; micalg="sha-256"; boundary="----39D1127DF0061CD9BB50644B14CCEF86"
    Date: Tue, 17 Mar 2020 20:02:11 +0100
    From: AliceRSA@example.com
    To: BobRSA@example.com
    Subject: Plain Text Message

    This is an S/MIME signed message

    ------39D1127DF0061CD9BB50644B14CCEF86
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit

    This a plain text body!
    ------39D1127DF0061CD9BB50644B14CCEF86
    Content-Type: application/x-pkcs7-signature; name="smime.p7s"
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename="smime.p7s"

    MIIEIwYJKoZIhvcNAQcCoIIEFDCCBBACAQExDzANBglghkgBZQMEAgEFADALBgkq
    hkiG9w0BBwGgggIwMIICLDCCAZWgAwIBAgIQRjRrx4AAVrwR024uxBCzsDANBgkq
    hkiG9w0BAQUFADASMRAwDgYDVQQDEwdDYXJsUlNBMB4XDTk5MDkxOTAxMDg0N1oX
    DTM5MTIzMTIzNTk1OVowEzERMA8GA1UEAxMIQWxpY2VSU0EwgZ8wDQYJKoZIhvcN
    AQEBBQADgY0AMIGJAoGBAOCJczmN2PX16Id2OX9OsAW7U4PeD7er3H3HdSkNBS5t
    Et+mhibU0m+qWCn8l+z6glEPMIC+sVCeRkTxLLvYMs/GaG8H2bBgrL7uNAlqE/X3
    BQWT3166NVbZYf8Zf8mB5vhs6odAcO+sbSx0ny36VTq5mXcCpkhSjE7zVzhXdFdf
    AgMBAAGjgYEwfzAMBgNVHRMBAf8EAjAAMA4GA1UdDwEB/wQEAwIGwDAfBgNVHSME
    GDAWgBTp4JAnrHggeprTTPJCN04irp44uzAdBgNVHQ4EFgQUd9K00bdMioqjzkWd
    zuw8oDrj/1AwHwYDVR0RBBgwFoEUQWxpY2VSU0FAZXhhbXBsZS5jb20wDQYJKoZI
    hvcNAQEFBQADgYEAPnBHqEjME1iPylFxa042GF0EfoCxjU3MyqOPzH1WyLzPbrMc
    WakgqgWBqE4lradwFHUv9ceb0Q7pY9Jkt8ZmbnMhVN/0uiVdfUnTlGsiNnRzuErs
    L2Tt0z3Sp0LF6DeKtNufZ+S9n/n+dO/q+e5jatg/SyUJtdgadq7rm9tJsCIxggG3
    MIIBswIBATAmMBIxEDAOBgNVBAMTB0NhcmxSU0ECEEY0a8eAAFa8EdNuLsQQs7Aw
    DQYJYIZIAWUDBAIBBQCggeQwGAYJKoZIhvcNAQkDMQsGCSqGSIb3DQEHATAcBgkq
    hkiG9w0BCQUxDxcNMjAwMzE3MTkwMzExWjAvBgkqhkiG9w0BCQQxIgQgUif5fULV
    gZhmFxie/WS5nFWC/LtbcHtu/+jQU6vglvQweQYJKoZIhvcNAQkPMWwwajALBglg
    hkgBZQMEASowCwYJYIZIAWUDBAEWMAsGCWCGSAFlAwQBAjAKBggqhkiG9w0DBzAO
    BggqhkiG9w0DAgICAIAwDQYIKoZIhvcNAwICAUAwBwYFKw4DAgcwDQYIKoZIhvcN
    AwICASgwDQYJKoZIhvcNAQEBBQAEgYAG/ZqevJVJYWtImeIG/HHVe0F6gXEpFx43
    FbsNV6kaFBOrfkgLICl/a6HaYu9xCHdS7bmiLlDs6qeofmyRAZgUBdDKySm+yjZc
    V1VLPuFuL9+BDcXarthOSnn4wbdRBhceRu7w8OnyoTtrwP58c0MiQVtyBQq1FuPZ
    WBKduWYjIg==

    ------39D1127DF0061CD9BB50644B14CCEF86--

Sign and Encrypt
################

The code below loads Alice's private and public key and also Bob's public key in PEM format and uses
it to sign and encrypt the e-mail (from Alice to Bob) in S/MIME format::


    import os
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from smail import sign_and_encrypt_message

    message = MIMEText("This a plain text body!")
    message['Date'] = formatdate(localtime=True)
    message['From'] = "AliceRSA@example.com"
    message['To'] = "BobRSA@example.com"
    message['Subject'] = "Text Message - Signed and Encrypted"

    key_signer = os.path.join('tests', 'testdata', 'AlicePrivRSASign.pem')
    cert_signer = os.path.join('tests', 'testdata', 'AliceRSASignByCarl.pem')

    cert = os.path.join('tests', 'testdata', 'BobRSASignByCarl.pem')

    signed_encrypted_message = sign_and_encrypt_message(message, key_signer, cert_signer, [cert])
    print(signed_encrypted_message.as_string())

Output::

    MIME-Version: 1.0
    Content-Type: application/pkcs7-mime; smime-type=enveloped-data; name=smime.p7m
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename=smime.p7m
    Date: Tue, 17 Mar 2020 20:05:34 +0100
    From: AliceRSA@example.com
    To: BobRSA@example.com
    Subject: Text Message - Signed and Encrypted

    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
    e3FI2iig5N6ytDwcN2MGTzr0SuhUe+JEQys2z2A=

Acknowledgements
================

**Python SMAIL** is heavily inspired by `python-smime`_ and is actually a fork of that code base. All credits go to
original Author(s).


License
=======

This software is licensed under the Apache License 2.0. See the LICENSE file in
the top distribution directory for the full license text.


Versioning
==========

This software follows `Semantic Versioning`_


.. _asn1crypto: https://github.com/wbond/asn1crypto
.. _oscrypto: https://github.com/wbond/oscrypto
.. _python-smime: https://github.com/balena/python-smime
.. _Semantic Versioning: http://semver.org/


