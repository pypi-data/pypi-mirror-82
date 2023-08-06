# *-* coding: utf-8 *-*

"""signer.py

Forked from https://github.com/m32/endesive/blob/master/endesive/signer.py

MIT License

Copyright (c) 2018 Grzegorz Makarewicz
Copyright (c) 2020 Robert Habermann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import hashlib
from datetime import datetime, timezone

from asn1crypto import cms, algos, core, x509
from oscrypto import asymmetric


def sign_bytes(data_unsigned, key_signer, cert_signer,
               digest_alg="sha256", sig_alg='rsa', attrs=True,
               include_cert_signer=True, additional_certs=None,
               signed_value=None, ):
    """Takes bytes, creates a ContentInfo structure and returns it as signed bytes

    Notes:
        cert_signer is mandatory (needed to get Issuer and Serial Number ) but can be
            excluded from signed data.

    Args:
        data_unsigned (bytes): data
        key_signer (:obj:`oscrypto.asymmetric.PrivateKey`): Private key used to sign the
            message.
        cert_signer (:obj:`asn1crypto.x509.Certificate`): Certificate/Public Key
            (belonging to Private Key) that will be included in the signed message.
        digest_alg (str): Digest (Hash) Algorithm - e.g. "sha256"
        sig_alg (str): Signature Algorithm
        attrs (bool): Whether to include signed attributes (signing time). Default
            to True
        include_cert_signer (bool): Whether to include the public certificate of the signer
            in the signed data. Default to True
        additional_certs (:obj:`list` of :obj:`asn1crypto.x509.Certificate`): List of
            additional certificates to be included (e.g. Intermediate or Root CA certs).
        signed_value: unknown


    Returns:
         bytes: signed bytes

    """

    if not isinstance(data_unsigned, bytes):
        raise AttributeError("only bytes supported")

    if not isinstance(key_signer, asymmetric.PrivateKey):
        raise AttributeError("only asn1crypto.keys.PrivateKeyInfo supported")

    if not isinstance(cert_signer, x509.Certificate):
        raise AttributeError("only asn1crypto.x509.Certificate supported")

    if include_cert_signer:
        certificates = [cert_signer]
    else:
        certificates = []

    if additional_certs:
        for additional in additional_certs:
            if not isinstance(additional, x509.Certificate):
                raise AttributeError("only asn1crypto.x509.Certificate supported")
            certificates.append(additional)

    if digest_alg not in ["md5", "sha1", "sha256", "sha512"]:
        raise AttributeError("digest algorithm unsupported: {}".format(digest_alg))

    if signed_value is None:
        signed_value = getattr(hashlib, digest_alg)(data_unsigned).digest()
    signed_time = datetime.now(tz=timezone.utc)

    signer = {
        'version': 'v1',
        'sid': cms.SignerIdentifier({
            'issuer_and_serial_number': cms.IssuerAndSerialNumber({
                'issuer': cert_signer.issuer,
                'serial_number': cert_signer.serial_number,
            }),
        }),
        'digest_algorithm': algos.DigestAlgorithm({'algorithm': digest_alg}),
        'signature': signed_value,
    }

    pss_digest_alg = digest_alg  # use same digest algorithm for pss signature as for message

    if sig_alg == "rsa":
        signer['signature_algorithm'] = algos.SignedDigestAlgorithm({'algorithm': 'rsassa_pkcs1v15'})

    elif sig_alg == "pss":
        salt_length = getattr(hashlib, pss_digest_alg)().digest_size
        signer['signature_algorithm'] = algos.SignedDigestAlgorithm({
            'algorithm': 'rsassa_pss',
            'parameters': algos.RSASSAPSSParams({
                'hash_algorithm': algos.DigestAlgorithm({'algorithm': pss_digest_alg}),
                'mask_gen_algorithm': algos.MaskGenAlgorithm({
                    'algorithm': algos.MaskGenAlgorithmId('mgf1'),
                    'parameters': {
                        'algorithm': algos.DigestAlgorithmId(pss_digest_alg),
                    }
                }),
                'salt_length': algos.Integer(salt_length),
                'trailer_field': algos.TrailerField(1)
            })
        })

    else:
        raise AttributeError("signature algorithm unsupported: {}".format(sig_alg))

    if attrs:
        if attrs is True:
            signer['signed_attrs'] = [
                cms.CMSAttribute({
                    'type': cms.CMSAttributeType('content_type'),
                    'values': ('data',),
                }),
                cms.CMSAttribute({
                    'type': cms.CMSAttributeType('message_digest'),
                    'values': (signed_value,),
                }),
                cms.CMSAttribute({
                    'type': cms.CMSAttributeType('signing_time'),
                    'values': (cms.Time({'utc_time': core.UTCTime(signed_time)}),)
                }),
            ]
        else:
            signer['signed_attrs'] = attrs

    config = {
        'version': 'v1',
        'digest_algorithms': cms.DigestAlgorithms((
            algos.DigestAlgorithm({'algorithm': digest_alg}),
        )),
        'encap_content_info': {
            'content_type': 'data',
        },
        'certificates': certificates,
        'signer_infos': [
            signer,
        ],
    }
    data_signed = cms.ContentInfo({
        'content_type': cms.ContentType('signed_data'),
        'content': cms.SignedData(config),
    })
    if attrs:
        to_sign = data_signed['content']['signer_infos'][0]['signed_attrs'].dump()
        to_sign = b'\x31' + to_sign[1:]
    else:
        to_sign = data_unsigned

    if sig_alg == "rsa":
        signed_value_signature = asymmetric.rsa_pkcs1v15_sign(key_signer, to_sign, digest_alg.lower())

    elif sig_alg == "pss":
        signed_value_signature = asymmetric.rsa_pss_sign(key_signer, to_sign, pss_digest_alg)

    else:
        raise AttributeError("signature algorithm unsupported: {}".format(sig_alg))

    data_signed['content']['signer_infos'][0]['signature'] = signed_value_signature

    return data_signed.dump()
