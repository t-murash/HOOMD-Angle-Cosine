// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

/*
  T. Murashima @ Tohoku University
 */


#include "hoomd/BondedGroupData.cuh"
#include "hoomd/ParticleData.cuh"
#include "hoomd/HOOMDMath.h"

/*! \file CosineAngleForceGPU.cuh
    \brief Declares GPU kernel code for calculating the cosine angle forces. 
    Used by CosineAngleForceComputeGPU.
*/

#ifndef __COSINEANGLEFORCEGPU_CUH__
#define __COSINEANGLEFORCEGPU_CUH__

//! Kernel driver that computes cosine angle forces for CosineAngleForceComputeGPU
cudaError_t gpu_compute_cosine_angle_forces(Scalar4* d_force,
					    Scalar* d_virial,
					    const unsigned int virial_pitch,
					    const unsigned int N,
					    const Scalar4 *d_pos,
					    const BoxDim& box,
					    const group_storage<3> *atable,
					    const unsigned int *apos_list,
					    const unsigned int pitch,
					    const unsigned int *n_angles_list,
					    Scalar2 *d_params,
					    unsigned int n_angle_types,
					    int block_size);

#endif
