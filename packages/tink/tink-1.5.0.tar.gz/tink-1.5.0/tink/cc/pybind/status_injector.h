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

#ifndef TINK_PYTHON_TINK_CC_PYBIND_STATUS_EXAMPLE_H_
#define TINK_PYTHON_TINK_CC_PYBIND_STATUS_EXAMPLE_H_

#include "pybind11/pybind11.h"

namespace pybind11 {
namespace test {

void PybindRegisterStatusInjector(pybind11::module* m);

}  // namespace test
}  // namespace pybind11

#endif  // TINK_PYTHON_TINK_CC_PYBIND_STATUS_EXAMPLE_H_
