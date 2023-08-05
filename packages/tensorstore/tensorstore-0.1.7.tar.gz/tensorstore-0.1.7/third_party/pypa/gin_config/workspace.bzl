# Copyright 2020 The TensorStore Authors
#
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
"""Defines a third-party bazel repo for the `gin-config` Python package."""

load(
    "//third_party:repo.bzl",
    "third_party_python_package",
)
load("//third_party:pypa/six/workspace.bzl", repo_pypa_six = "repo")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

def repo():
    repo_pypa_six()
    maybe(
        third_party_python_package,
        name = "pypa_gin_config",
        target = "gin_config",
        requirement = "gin-config==0.3.0",
        deps = [
            "@pypa_six//:six",
        ],
    )
