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

#ifndef TENSORSTORE_INDEX_SPACE_INTERNAL_IDENTITY_TRANSFORM_H_
#define TENSORSTORE_INDEX_SPACE_INTERNAL_IDENTITY_TRANSFORM_H_

#include "tensorstore/box.h"
#include "tensorstore/index_space/internal/transform_rep.h"

namespace tensorstore {
namespace internal_index_space {

/// Fills `maps` with identity mappings.
void SetToIdentityTransform(span<OutputIndexMap> maps);

/// Returns a newly allocated identity transform representation of the specified
/// rank that may be modified.
///
/// \dchecks rank >= 0
/// \remark The returned transform may be safely modified because
///     `reference_count == 1` except if `rank == 0`, in which case it is not
///     possible to modify anyway.
TransformRep::Ptr<> MakeIdentityTransform(DimensionIndex rank);

/// Returns a newly allocated identity transform representation with the
/// specified labels that may be modified.
TransformRep::Ptr<> MakeIdentityTransform(internal::StringLikeSpan labels);

/// Returns a newly allocated identity transform representation over the
/// specified input domain.
TransformRep::Ptr<> MakeIdentityTransform(BoxView<> domain);

/// Returns a newly allocated identity transform over the input domain of the
/// specified transform that may be modified.
///
/// \param data Non-null pointer to the existing transform representation.
/// \dchecks `data != nullptr`
TransformRep::Ptr<> MakeIdentityTransformLike(TransformRep* data);

/// Returns a newly allocated identity transform with an input_origin vector of
/// `0` and the specified `input_shape`.
TransformRep::Ptr<> MakeIdentityTransform(span<const Index> shape);

}  // namespace internal_index_space
}  // namespace tensorstore

#endif  // TENSORSTORE_INDEX_SPACE_INTERNAL_IDENTITY_TRANSFORM_H_
