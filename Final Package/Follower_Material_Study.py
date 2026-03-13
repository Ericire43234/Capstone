
# Import necessary function from src folder
from src import SF_Rectangular_Follower
import pandas as pd

if __name__ == "__main__":

    # Load material property database
    df = pd.read_excel("Data/BookMaterials.xlsx", skiprows=1)
    materials = df.iloc[:, 0].to_numpy()      # 0 : Material Name
    Epsi  = df.iloc[:, 1].to_numpy()          # 1 : Young's Modulus [psi]
    Sypsi = df.iloc[:, 2].to_numpy()          # 2 : Yield Strength [psi]

    material_dict = {
    name: [p1, p2,]
    for name, p1, p2, in zip(materials, Epsi, Sypsi)
    }    

    # Initialize dictionaries for storing results
    safe = {}
    unsafe = {}

    # Evaluate each material and classify based on safety factor
    for key in material_dict:
        value = material_dict[key]

        # Run beam calculation
        n, F, sa = SF_Rectangular_Follower(value[0],value[1])

        # Store results based on safety factor
        if n < 1:
            unsafe[key] = [n,F,sa]
        else:
            safe[key] = [n,F,sa]

    # Print out calculated values based on safety factor
    print("   ")
    print("Materials that are Unsafe for Use:")
    for key in unsafe:
        value = unsafe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f} psi')

    print("   ")
    print("Materials that are Safe for Use:")
    for key in safe:
        value = safe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f} psi')