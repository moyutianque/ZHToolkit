# Install Ros2 galactic with Mac M1 chip
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

This note is largely based on [link](http://mamykin.com/posts/building-ros2-on-macos-big-sur-m1/) but has fixed some issues not mentioned.


## Install prerequests
```bash
brew install direnv

# install python directly from brew
brew install bullet cmake cppcheck eigen pcre poco python tinyxml wget
python3 -m venv ~/.venv
echo "source ~/.venv/bin/activate" >> .envrc
pip install --upgrade pip && pip list

# other required packages
brew install asio tinyxml2
brew install opencv
brew install freeimage

brew install console_bridge
brew install openssl
echo "export OPENSSL_ROOT_DIR=$(brew --prefix openssl)" >> ~/.envrc

brew install log4cxx spdlog
brew install bison cunit
brew install qt@5 freetype assimp
brew install graphviz pyqt5 sip
echo "export Qt5_DIR=$(brew --prefix qt@5)/lib/cmake" >> ~/.envrc


echo "export PATH=$PATH:$(brew --prefix qt@5)/bin" >> ~/.bash_profile

# deal with pygraphviz error
echo "export GRAPHVIZ_DIR='/opt/homebrew/Cellar/graphviz/3.0.0'" >> ~/.bash_profile
source ~/.bash_profile
pip install pygraphviz --global-option=build_ext --global-option="-I$GRAPHVIZ_DIR/include" --global-option="-L$GRAPHVIZ_DIR/lib"

# other python packages
pip install -U \
 argcomplete catkin_pkg colcon-common-extensions coverage \
 cryptography empy flake8 flake8-blind-except flake8-builtins \
 flake8-class-newline flake8-comprehensions flake8-deprecated \
 flake8-docstrings flake8-import-order flake8-quotes ifcfg \
 importlib-metadata lark-parser lxml mock mypy netifaces \
 nose pep8 pydocstyle pydot pyparsing \
 pytest-mock rosdep setuptools vcstool psutil rosdistro

pip install matplotlib

```
## Get ros2 code
```bash
mkdir -p ~/ros2_galactic/src
cd ~/ros2_galactic
wget https://raw.githubusercontent.com/ros2/ros2/galactic/ros2.repos
vcs import src < ros2.repos
```

## Fix code problems for m1 chip

1. in ```src/osrf/osrf_testing_tools_cpp/osrf_testing_tools_cpp/src/memory_tools/vendor/bombela/backward-cpp/backward.hpp```

```bash
@@ -3927,8 +3927,10 @@ public:
     error_addr = reinterpret_cast<void *>(uctx->uc_mcontext.gregs[REG_EIP]);
 #elif defined(__arm__)
     error_addr = reinterpret_cast<void *>(uctx->uc_mcontext.arm_pc);
-#elif defined(__aarch64__)
+#elif defined(__aarch64__) && !defined(__APPLE__)
     error_addr = reinterpret_cast<void *>(uctx->uc_mcontext.pc);
+#elif defined(__APPLE__) && defined(__aarch64__)
+    error_addr = reinterpret_cast<void *>(uctx->uc_mcontext->__ss.__pc);
 #elif defined(__mips__)
     error_addr = reinterpret_cast<void *>(reinterpret_cast<struct sigcontext*>(&uctx->uc_mcontext)->sc_pc);
 #elif defined(__ppc__) || defined(__powerpc) || defined(__powerpc__) ||        \
```

2. in ```src/ros2/rviz/rviz_ogre_vendor/CMakeLists.txt```
```bash
diff --git a/CMakeLists.txt b/CMakeLists.txt
index faac7e1b..c36877c3 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -120,7 +120,7 @@ macro(build_ogre)
     set(OGRE_CXX_FLAGS "${OGRE_CXX_FLAGS} /w /EHsc")
   elseif(APPLE)
     set(OGRE_CXX_FLAGS "${OGRE_CXX_FLAGS} -std=c++14 -stdlib=libc++ -w")
-    list(APPEND extra_cmake_args "-DCMAKE_OSX_ARCHITECTURES='x86_64'")
+    list(APPEND extra_cmake_args "-DCMAKE_OSX_ARCHITECTURES='arm64'")
   else()  # Linux
     set(OGRE_C_FLAGS "${OGRE_C_FLAGS} -w")
     # include Clang -Wno-everything to disable warnings in that build. GCC doesn't mind it
```

3. in ```src/ros2/mimick_vendor/CMakeLists.txt```
```bash
- set(mimick_version "f171450b5ebaa3d2538c762a059dfc6ab7a01039")
+ set(mimick_version "4c742d61d4f47a58492c1afbd825fad1c9e05a09")
externalproject_add(mimick-${mimick_version}
```

4. in ```src/ros2/rviz/rviz_rendering/CMakeLists.txt```
```bash
- # Default to C++14
+ # Default to C++17
  if(NOT CMAKE_CXX_STANDARD)
-   set(CMAKE_CXX_STANDARD 14)
+   set(CMAKE_CXX_STANDARD 17)
```

5. after once build fix ```build/rviz_ogre_vendor/ogre-v1.12.1-prefix/src/ogre-v1.12.1/OgreMain/include/OgrePlatformInformation.h```
```bash
--- build/rviz_ogre_vendor/ogre-v1.12.1-prefix/src/ogre-v1.12.1/OgreMain/include/OgrePlatformInformation.h.orig	2021-06-02 16:28:58.000000000 -0400
+++ build/rviz_ogre_vendor/ogre-v1.12.1-prefix/src/ogre-v1.12.1/OgreMain/include/OgrePlatformInformation.h	2021-06-02 16:30:50.000000000 -0400
@@ -50,11 +50,11 @@
 #   define OGRE_CPU OGRE_CPU_X86

 #elif OGRE_PLATFORM == OGRE_PLATFORM_APPLE && defined(__BIG_ENDIAN__)
 #   define OGRE_CPU OGRE_CPU_PPC
 #elif OGRE_PLATFORM == OGRE_PLATFORM_APPLE
-#   define OGRE_CPU OGRE_CPU_X86
+#   define OGRE_CPU OGRE_CPU_ARM
 #elif OGRE_PLATFORM == OGRE_PLATFORM_APPLE_IOS && (defined(__i386__) || defined(__x86_64__))
 #   define OGRE_CPU OGRE_CPU_X86
 #elif defined(__arm__) || defined(_M_ARM) || defined(__arm64__) || defined(__aarch64__)
 #   define OGRE_CPU OGRE_CPU_ARM
 #elif defined(__mips64) || defined(__mips64_)
```

## Build Ros2
colcon build \
  --symlink-install \
  --merge-install \
  --event-handlers console_cohesion+ console_package_list+ \
  --packages-skip-by-dep python_qt_binding \
  --cmake-args \
    --no-warn-unused-cli \
    -DBUILD_TESTING=OFF \
    -DINSTALL_EXAMPLES=ON \
    -DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk \
    -DCMAKE_OSX_ARCHITECTURES="arm64" \
    -DCMAKE_PREFIX_PATH=$(brew --prefix):$(brew --prefix qt@5)
