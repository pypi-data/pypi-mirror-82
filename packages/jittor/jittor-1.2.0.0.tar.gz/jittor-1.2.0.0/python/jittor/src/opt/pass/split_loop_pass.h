// ***************************************************************
// Copyright (c) 2020 Jittor. Authors: Dun Liang <randonlang@gmail.com>. All Rights Reserved.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#pragma once
#include "opt/pass/pass.h"

namespace jittor {

struct SplitLoopPass : Pass {
    int number_of_ranges_after_split;

    SplitLoopPass() : Pass("split_loop"), number_of_ranges_after_split(0) {};
    void run() override;
};

} // jittor
