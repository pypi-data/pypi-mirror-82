# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tink.python.tink.streaming_aead_key_templates."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from tink.proto import aes_ctr_hmac_streaming_pb2
from tink.proto import aes_gcm_hkdf_streaming_pb2
from tink.proto import common_pb2
from tink.proto import tink_pb2
from tink import streaming_aead


class StreamingAeadKeyTemplatesTest(absltest.TestCase):

  def test_aes128_gcm_hkdf_4kb(self):
    template = streaming_aead.streaming_aead_key_templates.AES128_GCM_HKDF_4KB
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesGcmHkdfStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_gcm_hkdf_streaming_pb2.AesGcmHkdfStreamingKeyFormat()
    key_format.ParseFromString(template.value)

    self.assertEqual(16, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hkdf_hash_type)
    self.assertEqual(16, key_format.params.derived_key_size)
    self.assertEqual(4096, key_format.params.ciphertext_segment_size)

  def test_aes256_gcm_hkdf_4kb(self):
    template = streaming_aead.streaming_aead_key_templates.AES256_GCM_HKDF_4KB
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesGcmHkdfStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_gcm_hkdf_streaming_pb2.AesGcmHkdfStreamingKeyFormat()
    key_format.ParseFromString(template.value)

    self.assertEqual(32, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hkdf_hash_type)
    self.assertEqual(32, key_format.params.derived_key_size)
    self.assertEqual(4096, key_format.params.ciphertext_segment_size)

  def test_aes256_gcm_hkdf_1mb(self):
    template = streaming_aead.streaming_aead_key_templates.AES256_GCM_HKDF_1MB
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesGcmHkdfStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_gcm_hkdf_streaming_pb2.AesGcmHkdfStreamingKeyFormat()
    key_format.ParseFromString(template.value)

    self.assertEqual(32, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hkdf_hash_type)
    self.assertEqual(32, key_format.params.derived_key_size)
    self.assertEqual(1048576, key_format.params.ciphertext_segment_size)

  def test_aes128_ctr_hmac_sha256_4kb(self):
    template = (
        streaming_aead.streaming_aead_key_templates.AES128_CTR_HMAC_SHA256_4KB)
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesCtrHmacStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_ctr_hmac_streaming_pb2.AesCtrHmacStreamingKeyFormat()
    key_format.ParseFromString(template.value)

    self.assertEqual(16, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hkdf_hash_type)
    self.assertEqual(16, key_format.params.derived_key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hmac_params.hash)
    self.assertEqual(32, key_format.params.hmac_params.tag_size)
    self.assertEqual(4096, key_format.params.ciphertext_segment_size)

  def test_aes256_ctr_hmac_sha256_4kb(self):
    template = (
        streaming_aead.streaming_aead_key_templates.AES256_CTR_HMAC_SHA256_4KB)
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesCtrHmacStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_ctr_hmac_streaming_pb2.AesCtrHmacStreamingKeyFormat()
    key_format.ParseFromString(template.value)

    self.assertEqual(32, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hkdf_hash_type)
    self.assertEqual(32, key_format.params.derived_key_size)
    self.assertEqual(common_pb2.HashType.SHA256,
                     key_format.params.hmac_params.hash)
    self.assertEqual(32, key_format.params.hmac_params.tag_size)
    self.assertEqual(4096, key_format.params.ciphertext_segment_size)

  def test_create_aes_gcm_hkdf_streaming_key_template(self):
    # Intentionally using 'weird' or invalid values for parameters,
    # to test that the function correctly puts them in the resulting template.
    template = streaming_aead.streaming_aead_key_templates.create_aes_gcm_hkdf_streaming_key_template(
        aes_key_size=42,
        hash_type=common_pb2.HashType.SHA1,
        derived_key_size=76,
        ciphertext_segment_size=64,
    )
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesGcmHkdfStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_gcm_hkdf_streaming_pb2.AesGcmHkdfStreamingKeyFormat()
    key_format.ParseFromString(template.value)
    self.assertEqual(42, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA1, key_format.params.hkdf_hash_type)
    self.assertEqual(76, key_format.params.derived_key_size)
    self.assertEqual(64, key_format.params.ciphertext_segment_size)

  def test_create_aes_ctr_hmac_streaming_key_template(self):
    # Intentionally using 'weird' or invalid values for parameters,
    # to test that the function correctly puts them in the resulting template.
    template = streaming_aead.streaming_aead_key_templates.create_aes_ctr_hmac_streaming_key_template(
        aes_key_size=42,
        hkdf_hash_type=common_pb2.HashType.SHA1,
        derived_key_size=76,
        mac_hash_type=common_pb2.HashType.UNKNOWN_HASH,
        tag_size=39,
        ciphertext_segment_size=64,
    )
    self.assertEqual(
        'type.googleapis.com/google.crypto.tink.AesCtrHmacStreamingKey',
        template.type_url)
    self.assertEqual(tink_pb2.RAW, template.output_prefix_type)
    key_format = aes_ctr_hmac_streaming_pb2.AesCtrHmacStreamingKeyFormat()
    key_format.ParseFromString(template.value)
    self.assertEqual(42, key_format.key_size)
    self.assertEqual(common_pb2.HashType.SHA1, key_format.params.hkdf_hash_type)
    self.assertEqual(76, key_format.params.derived_key_size)
    self.assertEqual(common_pb2.HashType.UNKNOWN_HASH,
                     key_format.params.hmac_params.hash)
    self.assertEqual(39, key_format.params.hmac_params.tag_size)
    self.assertEqual(64, key_format.params.ciphertext_segment_size)


if __name__ == '__main__':
  absltest.main()
