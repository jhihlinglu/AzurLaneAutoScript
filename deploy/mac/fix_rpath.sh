#!/bin/bash
# Fix duplicate LC_RPATH entries in the 'alas' conda environment.
#
# macOS 12+ rejects duplicate rpaths anywhere in the dynamic library load chain.
# Packages from the anaconda channel often contain duplicate @loader_path entries
# that cause ImportError when loading numpy, mxnet, or opencv.
#
# Run this script once after creating the conda environment:
#   CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml
#   bash deploy/mac/fix_rpath.sh
#
# Tested on: macOS 14 (Sonoma), Apple Silicon (M-series), miniforge3

set -e

ENV_LIB="${CONDA_PREFIX:-$(conda info --base)/envs/alas}/lib"

if [ ! -d "$ENV_LIB" ]; then
    echo "Error: conda env lib not found at $ENV_LIB"
    echo "Please activate the alas environment first: conda activate alas"
    exit 1
fi

echo "Fixing duplicate rpaths in: $ENV_LIB"

# Step 1: Fix exact-duplicate LC_RPATH entries across all dylibs and .so files
find "$ENV_LIB" \( -name "*.dylib" -o -name "*.so" \) | while read -r lib; do
    rpaths=$(otool -l "$lib" 2>/dev/null | awk '/LC_RPATH/{found=1} found && /path /{print $2; found=0}')
    dupes=$(echo "$rpaths" | sort | uniq -d)
    if [ -n "$dupes" ]; then
        echo "  Fixing: $(basename "$lib")"
        while IFS= read -r dupe; do
            install_name_tool -delete_rpath "$dupe" "$lib" 2>/dev/null || true
        done <<< "$dupes"
        codesign -f -s - "$lib" 2>/dev/null || true
    fi
done

# Step 2: Fix libopenblas specifically — it uses @rpath for libgfortran/libomp
# which causes chain-level duplicate rpath conflicts with numpy's own rpath.
# Solution: change @rpath references to @loader_path and remove all LC_RPATH entries.
OPENBLAS="$ENV_LIB/libopenblas.0.dylib"
if [ -f "$OPENBLAS" ]; then
    echo "  Fixing: libopenblas.0.dylib (chain rpath conflict)"
    install_name_tool \
        -change "@rpath/libgfortran.5.dylib" "@loader_path/libgfortran.5.dylib" \
        -change "@rpath/libomp.dylib"         "@loader_path/libomp.dylib" \
        -change "@rpath/libopenblas.0.dylib"  "@loader_path/libopenblas.0.dylib" \
        "$OPENBLAS" 2>/dev/null || true
    for rpath in $(otool -l "$OPENBLAS" | awk '/LC_RPATH/{found=1} found && /path /{print $2; found=0}'); do
        install_name_tool -delete_rpath "$rpath" "$OPENBLAS" 2>/dev/null || true
    done
    codesign -f -s - "$OPENBLAS"
fi

echo "Done. All rpath issues fixed."
