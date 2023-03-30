The use of meson to build numtypes is work-in-progress.

To build (but not install) with meson, run

```
meson setup build --prefix $(pwd)/build-install
meson install -C build
```

To use the build, add build-install/lib/python3.10/site-packages/ to PYTHONPATH.
