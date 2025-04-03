import h5py
import numpy as np

def analyze_hdf5(file_path):
    """
    Analiza un archivo .hdf5 e imprime sus claves y datos.
    """
    print(f"\nAnalizando archivo: {file_path}")
    with h5py.File(file_path, 'r') as f:
        for key in f.keys():
            data = f[key]
            print(f"Clave: {key}")
            print(f"  Tipo de dato: {type(data)}")
            if isinstance(data, h5py.Dataset):
                print(f"  Forma: {data.shape}")
                print(f"  Tipo: {data.dtype}")
                if data.size < 10:  # Imprimir valores si son pocos
                    print(f"  Valores: {data[()]}")
                else:
                    print(f"  Valores (primeros 10): {data[()][:10]}")
            elif isinstance(data, h5py.Group):
                print(f"  Grupo con claves: {list(data.keys())}")

def compare_hdf5(file1, file2):
    """
    Compara dos archivos .hdf5 e identifica diferencias en claves y datos.
    """
    print(f"\nComparando archivos:\n  {file1}\n  {file2}")
    with h5py.File(file1, 'r') as f1, h5py.File(file2, 'r') as f2:
        keys1 = set(f1.keys())
        keys2 = set(f2.keys())

        # Comparar claves
        print("\nClaves únicas en el primer archivo:")
        print(keys1 - keys2)
        print("\nClaves únicas en el segundo archivo:")
        print(keys2 - keys1)

        # Comparar datos comunes
        common_keys = keys1 & keys2
        for key in common_keys:
            data1 = f1[key][()]
            data2 = f2[key][()]
            if np.array_equal(data1, data2):
                print(f"\nClave común '{key}': Los datos son iguales.")
            else:
                print(f"\nClave común '{key}': Los datos son diferentes.")
                print(f"  Datos del primer archivo (primeros 10): {data1[:10]}")
                print(f"  Datos del segundo archivo (primeros 10): {data2[:10]}")

# Rutas de los archivos .hdf5
file_generated = "/bodega/FPM/PtyLab/FPM_generator-master/FPM_generator-master/Resultados/result1.hdf5"  # Archivo generado por el código actual
file_reference = "/bodega/FPM/USAFTargetFPM.hdf5"  # Archivo que funciona correctamente

# Analizar ambos archivos
analyze_hdf5(file_generated)
analyze_hdf5(file_reference)

# Comparar ambos archivos
compare_hdf5(file_generated, file_reference)
