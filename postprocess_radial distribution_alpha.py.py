#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:40:13 2025

@author: ashish
"""

import os
import vtk
import numpy as np
import matplotlib.pyplot as plt

# Define folder path and target VTM file
folder_path = ""
target_vtm = os.path.join(folder_path, "case10_100000.vtm")

# Define multiple alpha.particles threshold values
height =0.27
bed_heights = []  # Store bed heights for each threshold
initial_bed_height = 0.246  # Reference height for expansion calculation
centroid_at_height= []
alpha_at_height = []
cell_volume_at_height = []

# Check if the VTM file exists
if os.path.exists(target_vtm):
    print(f"\nProcessing: {target_vtm}")

    # Create a VTK MultiBlock reader
    reader = vtk.vtkXMLMultiBlockDataReader()
    reader.SetFileName(target_vtm)
    reader.Update()

    # Get the MultiBlock dataset
    multiblock_data = reader.GetOutput()
    num_blocks = multiblock_data.GetNumberOfBlocks()
    print(f"  ➜ Number of Blocks: {num_blocks}")
    # Loop through all blocks
    for i in range(num_blocks):
        block = multiblock_data.GetBlock(i)

        # Check if block is a valid vtkUnstructuredGrid
        if isinstance(block, vtk.vtkUnstructuredGrid):
            print(f"    - Block {i}: {block.GetNumberOfCells()} Cells")

            # Extract cell data
            cell_data = block.GetCellData()
            alpha_array = cell_data.GetArray("alpha.particles")
            
            quality_filter = vtk.vtkMeshQuality()
            quality_filter.SetInputData(block)
            quality_filter.SetTetQualityMeasureToVolume()
            quality_filter.Update()
            cell_qualities = quality_filter.GetOutput().GetCellData().GetArray("Quality")
            
            for j in range(block.GetNumberOfCells()):
                cell = block.GetCell(j)
                points = cell.GetPoints()
                num_pts = points.GetNumberOfPoints()
                centroid = np.mean([points.GetPoint(k) for k in range(num_pts)], axis=0)
                alpha_value = alpha_array.GetValue(j)
                cell_volume = cell_qualities.GetValue(j)
                
                if abs(centroid[1] - height) < 0.002:
                    centroid_at_height.append(centroid)
                    alpha_at_height.append(alpha_value)
                    cell_volume_at_height.append(cell_volume)
                    
else:
    print(f"❌ Error: {target_vtm} not found!")  

centroid_at_height = np.array(centroid_at_height)
alpha_at_height = np.array(alpha_at_height)

dist = []
for i in centroid_at_height:
    di = np.sqrt(i[0]**2 + i[2]**2)  # radial distance in XZ plane
    dist.append(di)

dist = np.sort(dist)

unique = []
temp = [dist[0]]  # start with the first value

for i in range(1, len(dist)):
    if abs(dist[i] - dist[i - 1]) <= 0.0002:
        temp.append(dist[i])
    else:
        avg = np.average(temp)
        unique.append(avg)
        temp = [dist[i]]  # start a new group

# After loop, add the last group
if temp:
    avg = np.average(temp)
    unique.append(avg)


#unique.append(len(dist))

#for i in dist:
 #   if np.isin(unique,i).any()== False:
  #      unique.append(i)

print(centroid_at_height.size)

index = []

for i in range(len(unique)):
    t = []
    for j in range(len(centroid_at_height)):
        dist_j = np.sqrt(centroid_at_height[j][0]**2 + centroid_at_height[j][2]**2)
        if abs(dist_j - unique[i]) <= 0.0002:
            t.append(j)
    index.append(t)  # move this outside inner loop

import matplotlib.pyplot as plt

# Compute volume-weighted average alpha.particles for each radial bin
avg_alpha = []

for idx_list in index:
    if len(idx_list) == 0:
        avg_alpha.append(0)
        continue
    total_volume = sum(cell_volume_at_height[i] for i in idx_list)
    weighted_alpha = sum(alpha_at_height[i] * cell_volume_at_height[i] for i in idx_list)
    avg_alpha.append(weighted_alpha / total_volume if total_volume != 0 else 0)

# Plot average alpha.particles vs radial distance
plt.figure(figsize=(7, 5))
plt.plot(unique, avg_alpha, marker='o', linestyle='-', color='navy')
plt.xlabel("Radial Distance (m)")
plt.ylabel("Average α.particles")
plt.title(f"Radial Distribution of α.particles at Height = {height} m case10")
plt.ylim(0,0.7)
plt.grid(True)
plt.tight_layout()
plt.show()
  
        
        
        
    
    
    


                    
                    
                    