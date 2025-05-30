import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def plot_polygon_from_file(filepath, labels):
    """
    Reads a file of points in "x,y" format (one point per line),
    constructs a polygon connecting them in order, plots it, and
    labels each vertex according to `labels`.
    
    Args:
        filepath (str): Path to text file.
        labels (List[str]): A list of labels for each point, in
                             the same order as the file.
    """
    # Read points from file
    points = []
    with open(filepath, 'r') as f:
        for line in f:
            x_str, y_str = line.strip().split(',')
            points.append((float(x_str), float(y_str)))

    if len(points) != len(labels):
        raise ValueError(f"Expected {len(labels)} points, found {len(points)}")

    # Separate x and y for plotting limits
    xs, ys = zip(*points)

    # Create plot
    fig, ax = plt.subplots()
    # Draw filled polygon
    polygon = Polygon(points, closed=True, fill=True, edgecolor='blue', linewidth=2, alpha=0.3)
    ax.add_patch(polygon)
    # Plot and label each corner
    for (x, y), lbl in zip(points, labels):
        ax.scatter(x, y, color='red')
        ax.text(
            x, y, lbl,
            fontsize=12,
            fontweight='bold',
            ha='right',  # horizontal alignment
            va='bottom'  # vertical alignment
        )

    # Set plot limits with padding
    padding = 1
    ax.set_xlim(min(xs) - padding, max(xs) + padding)
    ax.set_ylim(min(ys) - padding, max(ys) + padding)

    ax.set_title(f'Polygon from {filepath}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    labels = ["top_left", "top_right", "bottom_right", "bottom_left"]
    plot_polygon_from_file('/home/jasper/frustum.txt', labels)
