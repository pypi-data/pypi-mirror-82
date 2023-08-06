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

#include "tink/integration/awskms/aws_kms_client.h"

#include "pybind11/pybind11.h"
#include "tink/util/statusor.h"
#include "tink/cc/pybind/status_casters.h"


namespace crypto {
namespace tink {
namespace integration {
namespace awskms {

void PybindRegisterCcAwsKmsClient(pybind11::module* module) {
  namespace py = pybind11;
  py::module& m = *module;

  py::class_<AwsKmsClient>(
      m, "AwsKmsClient",
      "Wrapper for C++ AwsKMS."
      )
      .def(py::init([](const std::string& key_uri,
                       const std::string& credentials_path) {
        auto client_result = AwsKmsClient::New(key_uri, credentials_path);
        if (!client_result.ok()) {
          throw pybind11::value_error("Could not create client.");
        }
        return std::move(client_result.ValueOrDie());
      }))
      .def(
          "does_support",
          [](const AwsKmsClient& self, const std::string& key_uri) -> bool {
            return self.DoesSupport(key_uri);
          },
          py::arg("key_uri"), "URI of the key to be checked.")
      .def(
          "get_aead",
          [](const AwsKmsClient& self, const std::string& key_uri) ->
          util::StatusOr<std::unique_ptr<Aead>> {
            return self.GetAead(key_uri);
          },
          py::arg("key_uri"), "URI of the key which should be used.")
      .def_static(
          "register_client",
          [](const std::string& key_uri,
             const std::string& credentials_path) -> util::Status {
            return AwsKmsClient::RegisterNewClient(key_uri, credentials_path);
          },
          py::arg("key_uri"), "URI of the key which should be used.",
          py::arg("credentials_path"),
          "Path to the credentials for the client.");
}

}  // namespace awskms
}  // namespace integration
}  // namespace tink
}  // namespace crypto
