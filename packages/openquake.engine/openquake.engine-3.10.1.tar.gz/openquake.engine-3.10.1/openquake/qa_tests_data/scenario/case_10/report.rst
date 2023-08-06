Hazard France Reduced
=====================

============== ===================
checksum32     3_844_410_873      
date           2020-03-13T11:20:15
engine_version 3.9.0-gitfb3ef3a732
============== ===================

num_sites = 66, num_levels = 0, num_rlzs = 1

Parameters
----------
=============================== ===============
calculation_mode                'scenario'     
number_of_logic_tree_samples    0              
maximum_distance                None           
investigation_time              None           
ses_per_logic_tree_path         1              
truncation_level                None           
rupture_mesh_spacing            5.0            
complex_fault_mesh_spacing      5.0            
width_of_mfd_bin                None           
area_source_discretization      None           
pointsource_distance            {'default': {}}
ground_motion_correlation_model None           
minimum_intensity               {}             
random_seed                     42             
master_seed                     0              
ses_seed                        42             
=============================== ===============

Input files
-----------
======== ============================================
Name     File                                        
======== ============================================
exposure `Exposure_France.xml <Exposure_France.xml>`_
job_ini  `job.ini <job.ini>`_                        
======== ============================================

Composite source model
----------------------
========= ======= ================
smlt_path weight  num_realizations
========= ======= ================
b_1       1.00000 1               
========= ======= ================

Exposure model
--------------
=========== ==
#assets     66
#taxonomies 22
=========== ==

======================= ======= ======= === === ========= ==========
taxonomy                mean    stddev  min max num_sites num_assets
CR/LWAL+CDN/H:2         1.00000 NaN     1   1   1         1         
W/LWAL+CDN/H:2          1.00000 0.0     1   1   5         5         
MUR+CL/LWAL+CDN/H:2     1.00000 0.0     1   1   7         7         
CR/LFINF+CDM/HBET:3-5   1.00000 0.0     1   1   2         2         
CR/LFINF+CDM/H:2        1.00000 0.0     1   1   8         8         
CR/LWAL+CDM/H:2         1.00000 0.0     1   1   7         7         
MUR+CL/LWAL+CDN/H:1     1.00000 0.0     1   1   2         2         
CR/LFINF+CDM/H:1        1.00000 0.0     1   1   6         6         
MUR+ST/LWAL+CDN/H:1     1.00000 0.0     1   1   7         7         
W/LWAL+CDN/H:1          1.00000 0.0     1   1   2         2         
W/LWAL+CDM/H:1          1.00000 0.0     1   1   3         3         
CR/LWAL+CDN/HBET:3-5    1.00000 NaN     1   1   1         1         
W/LWAL+CDM/H:2          1.00000 NaN     1   1   1         1         
CR/LWAL+CDM/H:1         1.00000 0.0     1   1   2         2         
CR/LWAL+CDM/HBET:3-5    1.00000 0.0     1   1   3         3         
MUR+CL/LWAL+CDM/H:2     1.00000 NaN     1   1   1         1         
CR+PC/LWAL+CDM/HBET:3-5 1.00000 0.0     1   1   2         2         
CR/LWAL+CDH/H:2         1.00000 NaN     1   1   1         1         
CR/LWAL+CDH/HBET:3-5    1.00000 0.0     1   1   2         2         
MUR+ST/LWAL+CDN/H:2     1.00000 NaN     1   1   1         1         
CR/LFINF+CDH/H:1        1.00000 NaN     1   1   1         1         
CR/LFINF+CDH/H:2        1.00000 NaN     1   1   1         1         
*ALL*                   0.00964 0.09774 0   1   6_843     66        
======================= ======= ======= === === ========= ==========

Information about the tasks
---------------------------
Not available

Data transfer
-------------
==== ==== ========
task sent received
==== ==== ========

Slowest operations
------------------
================ ======== ========= ======
calc_66865       time_sec memory_mb counts
================ ======== ========= ======
reading exposure 0.01383  0.0       1     
================ ======== ========= ======