// ***************************************************************
// Copyright (c) 2020 Jittor. Authors: Dun Liang <randonlang@gmail.com>. All Rights Reserved.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#pragma once
#include <functional>

using namespace std;

void test_main();

void on_error() {
    throw std::exception();
}

void expect_error(function<void()> func) {
    try {
        func();
    } catch (...) {
        return;
    }
    CHECK(0) << "Missing error";
}

int main() {
    try {
        test_main();
    } catch (...) {
        return 1;
    }
}