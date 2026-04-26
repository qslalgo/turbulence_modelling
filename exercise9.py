import pandas as pd
import re

def read_txt_file(file_path):
    # Read the file
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Get the variable names
    variables = []
    dataframes = []
    current_zone = None
    data_block = []

    for line in lines:
        # Get variable names
        if "VARIABLES" in line:
            # Clean up the line to get variable names
            variables = [v.strip().strip('"') for v in line.split("=")[1].split(",")]

        # Detect new ZONE
        elif line.strip().startswith("ZONE"):
            if data_block:
                # Save previous data block
                df = pd.DataFrame(data_block, columns=[f"{v}_{current_zone}" for v in variables])
                dataframes.append(df)
                data_block = []

            # Extract zone identifier
            match = re.search(r'x/Dj\s*=\s*(\d+)', line)
            if match:
                current_zone = f"x{match.group(1)}"

        # Parse data lines
        elif re.match(r"^[\d\.\-\+E]+", line.strip()):
            nums = list(map(float, line.strip().split()))
            data_block.append(nums)

    # Don't forget the last block
    if data_block:
        df = pd.DataFrame(data_block, columns=[f"{v}_{current_zone}" for v in variables])
        dataframes.append(df)

    # Combine all zone-specific data horizontally
    final_df = pd.concat(dataframes, axis=1)

    # Optionally save or inspect
    # final_df.to_csv("jet_data_combined.csv", index=False)
    return final_df

file = r'exercise9/jet-nasa-data.txt'
file2= r'exercise9/jet-nasa-data-axis.txt'
df_nasa = read_txt_file(file)
df_nasa_axis = read_txt_file(file2)
df_nasa





def reading_jet_file_nasa(
    FILE,
    xlabel=None,
    ylabel=None,
    title=None,
    legend_labels=None,
    style_kwargs=None,
    data_nasa=None,  # Pass your experimental dataframe here
    nasa_quantity_y=None,  # e.g., "k/Uj^2"
    nasa_quantity_x=None,
    nasa_style=None,  # e.g., {"marker": "s", "linestyle": "None"}
):
    import pandas as pd
    import matplotlib.pyplot as plt
    import re

    # === READ SIMULATION DATA ===
    with open(FILE, "r") as f:
        content = f.read()

    labels_match = re.search(r'\(labels\s+"([^"]+)"\s+"([^"]+)"\)', content)
    if labels_match:
        label1, label2 = labels_match.groups()
    else:
        raise ValueError("Could not find labels.")

    xlabel = xlabel or label1
    ylabel = ylabel or label2
    title = title or f"{ylabel} vs. {xlabel}"

    blocks = re.findall(
        r'\(xy/key/label\s+"([^"]+)"\)\s*((?:-?\d*\.?\d+(?:[eE][\+\-]?\d+)?\s+-?\d*\.?\d+(?:[eE][\+\-]?\d+)?\s*\n?)+)',
        content
    )

    dfs = []
    keys = []
    for key, data_block in blocks:
        keys.append(key)
        data = [
            list(map(float, line.strip().split()))
            for line in data_block.strip().splitlines()
            if line.strip()
        ]
        df = pd.DataFrame(data, columns=[f"{label1}_{key}", f"{label2}_{key}"])
        dfs.append(df)

    final_df = pd.concat(dfs, axis=1)

    # === PLOTTING ===
    plt.figure(figsize=(8, 6))
    
    # Plot simulation data
    for i, df in enumerate(dfs):
        x_col = df.columns[0]
        y_col = df.columns[1]
        label = legend_labels[i] if legend_labels and i < len(legend_labels) else y_col

        if style_kwargs:
            plt.plot(df[x_col], df[y_col], label=f"Sim {label}", **style_kwargs)
        else:
            plt.plot(df[x_col], df[y_col], label=f"Sim {label}")

    # Plot experimental NASA data
    if data_nasa is not None and nasa_quantity_x and nasa_quantity_y is not None:
        for x_loc in [10, 15, 20, 2, 5]:  # You can change these as needed
            x_col = f"{nasa_quantity_x}_x{x_loc}"
            y_col = f"{nasa_quantity_y}_x{x_loc}"
            if x_col in data_nasa.columns and y_col in data_nasa.columns:
                plt.plot(
                    data_nasa[x_col],
                    data_nasa[y_col],
                    label=f"Exp x/D={x_loc}",
                    **(nasa_style if nasa_style else {"marker": None, "linestyle": "--"})
                )

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlim(left=-0.0001)  # Set x-axis limit to start from 0
    plt.ylim(bottom=0)  # Set y-axis limit to start from 0
    plt.legend()
    plt.tight_layout()
    plt.show()

    return '<3'





reading_jet_file_nasa(
    FILE="exercise9/turb5-y-over-d-jet-k-over-u-jet2.xy",
    xlabel=r'$k/U_{jet}^2$',
    ylabel=r'$y/D_{jet}$',
    title=r'$y/D_{jet}$ vs. $k/U_{jet}^2$ Profile',
    legend_labels=[r'$x/D_{jet}=10$', r'$x/D_{jet}=15$', r'$x/D_{jet}=20$', r'$x/D_{jet}=2$', r'$x/D_{jet}=5$'],
    data_nasa=df_nasa,
    nasa_quantity_y='y/Dj',
    nasa_quantity_x="k/Uj^2",
    nasa_style={"marker": "None", "linestyle": "--"}
)	

reading_jet_file_nasa(
    FILE="exercise9/turb5-y-over-d-jet-u-over-u-jet.xy",
    xlabel=r'$u/U_{jet}$',
    ylabel=r'$y/D_{jet}$',
    title=r'$y/D_{jet}$ vs. $u/U_{jet}$ Profile',
    legend_labels=[r'$x/D_{jet}=10$', r'$x/D_{jet}=15$', r'$x/D_{jet}=20$', r'$x/D_{jet}=2$', r'$x/D_{jet}=5$'],
    data_nasa=df_nasa,
    nasa_quantity_y='y/Dj',
    nasa_quantity_x="u/Uj",
    nasa_style={"marker": "None", "linestyle": "--"}
)

reading_jet_file_nasa(
    FILE="exercise9/turb5-y-over-d-jet-uv-over-u-jet2.xy",
    xlabel=r'$uv/U_{jet}^2$',
    ylabel=r'$y/D_{jet}$',
    title=r'$y/D_{jet}$ vs. $uv/U_{jet}^2$ Profile',
    legend_labels=[r'$x/D_{jet}=10$', r'$x/D_{jet}=15$', r'$x/D_{jet}=20$', r'$x/D_{jet}=2$', r'$x/D_{jet}=5$'],
    data_nasa=df_nasa,
    nasa_quantity_y='y/Dj',
    nasa_quantity_x="u'v'/Uj^2",
    nasa_style={"marker": "None", "linestyle": "--"}
)

reading_jet_file_nasa(
    FILE="exercise9/turb5-y-over-d-jet-v-over-u-jet.xy",
    xlabel=r'$v/U_{jet}$',
    ylabel=r'$y/D_{jet}$',
    title=r'$y/D_{jet}$ vs. $v/U_{jet}$ Profile',
    legend_labels=[r'$x/D_{jet}=10$', r'$x/D_{jet}=15$', r'$x/D_{jet}=20$', r'$x/D_{jet}=2$', r'$x/D_{jet}=5$'],
    data_nasa=df_nasa,
    nasa_quantity_y='y/Dj',
    nasa_quantity_x="v/Uj",
    nasa_style={"marker": "None", "linestyle": "--"}
)



reading_jet_file_nasa(
    FILE="exercise9/turb5-y-over-d-jet-v-over-u-jet.xy",
    xlabel=r'$v/U_{jet}$',
    ylabel=r'$y/D_{jet}$',
    title=r'$y/D_{jet}$ vs. $v/U_{jet}$ Profile',
    legend_labels=[r'$x/D_{jet}=10$', r'$x/D_{jet}=15$', r'$x/D_{jet}=20$', r'$x/D_{jet}=2$', r'$x/D_{jet}=5$'],
    data_nasa=df_nasa,
    nasa_quantity_y='y/Dj',
    nasa_quantity_x="v/Uj",
    nasa_style={"marker": "None", "linestyle": "--"}
)
