import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

def load_data(file_path):
    df = pd.read_csv(file_path)
    frames = []
    num_points = (len(df.columns) - 1) // 3
    
    for _, row in df.iterrows():
        frame_points = []
        for i in range(num_points):
            x = row[f'{i}_x [m]']
            y = row[f'{i}_y [m]']
            z = row[f'{i}_z [m]']
            frame_points.append([x, y, z])
        frames.append(frame_points)
    
    return np.array(frames)

def update(frame_num, scatter, frames_data, ax):
    # 更新點
    scatter._offsets3d = (frames_data[frame_num,:,0],
                        frames_data[frame_num,:,1],
                        frames_data[frame_num,:,2])
    
    ax.set_title(f'Frame: {frame_num}')
    return scatter,

def create_animation(frames_data, output_path='points_animation.gif'):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    
    x_min, x_max = np.nanmin(frames_data[:,:,0]), np.nanmax(frames_data[:,:,0])
    y_min, y_max = np.nanmin(frames_data[:,:,1]), np.nanmax(frames_data[:,:,1])
    z_min, z_max = np.nanmin(frames_data[:,:,2]), np.nanmax(frames_data[:,:,2])
    
    margin = 0.1
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min
    
    ax.set_xlim([x_min - margin * x_range, x_max + margin * x_range])
    ax.set_ylim([y_min - margin * y_range, y_max + margin * y_range])
    ax.set_zlim([z_min - margin * z_range, z_max + margin * z_range])
    
    scatter = ax.scatter(frames_data[0,:,0],
                        frames_data[0,:,1],
                        frames_data[0,:,2],
                        c='red',
                        s=50)
    
    ax.view_init(elev=20, azim=45)
    anim = FuncAnimation(fig, update,
                        frames=len(frames_data),
                        fargs=(scatter, frames_data, ax),
                        interval=50,
                        blit=True)
    
    anim.save(output_path, writer='pillow', fps=20)
    plt.close()
    print(f'done')

def main():
    frames_data = load_data('hit48_threeD_post.csv')
    create_animation(frames_data)

if __name__ == "__main__":
    main()