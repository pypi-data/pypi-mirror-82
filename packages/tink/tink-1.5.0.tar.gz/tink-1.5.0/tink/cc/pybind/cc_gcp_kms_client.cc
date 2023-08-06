// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
///////////////////////////////////////////////////////////////////////////////

#include "pybind11/pybind11.h"
#include "tink/integration/gcpkms/gcp_kms_client.h"
#include "tink/kms_clients.h"
#include "tink/util/statusor.h"
#include "tink/cc/pybind/status_casters.h"

namespace crypto {
namespace tink {
namespace integration {
namespace gcpkms {

void PybindRegisterCcGcpKmsClient(pybind11::module* module) {
  namespace py = pybind11;
  py::module& m = *module;

  py::class_<GcpKmsClient>(m, "GcpKmsClient", "Wrapper for C++ GcpKMS.")
      .def(py::init(
          [](const std::string& key_uri, const std::string& credentials_path) {
            auto client_result = GcpKmsClient::New(key_uri, credentials_path);
            if (!client_result.ok()) {
              throw pybind11::value_error("Could not create client.");
            }

            return std::move(client_result.ValueOrDie());
          }))
      .def(
          "does_support",
          [](const GcpKmsClient& self, const std::string& key_uri) -> bool {
            return self.DoesSupport(key_uri);
          },
          py::arg("key_uri"), "URI of the key to be checked.")
      .def(
          "get_aead",
          [](const GcpKmsClient& self, const std::string& key_uri)
              -> util::StatusOr<std::unique_ptr<Aead>> {
            return self.GetAead(key_uri);
          },
          py::arg("key_uri"), "URI of the key which should be used.")
      .def_static(
          "register_client",
          [](const std::string& key_uri,
             const std::string& credentials_path) -> util::Status {
            return GcpKmsClient::RegisterNewClient(key_uri, credentials_path);
          },
          py::arg("key_uri"), "URI of the key which should be used.",
          py::arg("credentials_path"),
          "Path to the credentials for the client.");
}

}  // namespace gcpkms
}  // namespace integration
}  // namespace tink
}  // namespace crypto
