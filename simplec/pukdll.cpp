#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT int puk(int i) {
    return i + 36;
}
