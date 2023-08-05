// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef TENSORSTORE_INTERNAL_ATTRIBUTES_H_
#define TENSORSTORE_INTERNAL_ATTRIBUTES_H_

#include "absl/base/attributes.h"

#if ABSL_HAVE_ATTRIBUTE(no_unique_address)
#define TENSORSTORE_ATTRIBUTE_NO_UNIQUE_ADDRESS [[no_unique_address]]
#else
#define TENSORSTORE_ATTRIBUTE_NO_UNIQUE_ADDRESS
#endif

#endif  // TENSORSTORE_INTERNAL_ATTRIBUTES_H_
