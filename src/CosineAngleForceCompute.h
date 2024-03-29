// Copyright (c) 2021-2022 Takahiro Murashima @ Tohoku University
// under the BSD 3-Clause License.

#include "hoomd/BondedGroupData.h"
#include "hoomd/ForceCompute.h"

#include <memory>
#include <vector>

/*! \file CosineAngleForceCompute.h
    \brief Declares a class for computing cosine angles
*/

#ifdef __HIPCC__
#error This header cannot be compiled by nvcc
#endif

#include <pybind11/pybind11.h>

#ifndef __COSINEANGLEFORCECOMPUTE_H__
#define __COSINEANGLEFORCECOMPUTE_H__

namespace hoomd
    {
namespace md
    {
struct cosine_params
    {
    Scalar k;
    Scalar t_0;

#ifndef __HIPCC__
    cosine_params() : k(0), t_0(0) { }

    cosine_params(pybind11::dict params)
        : k(params["k"].cast<Scalar>()), t_0(params["t0"].cast<Scalar>())
        {
        }

    pybind11::dict asDict()
        {
        pybind11::dict v;
        v["k"] = k;
        v["t0"] = t_0;
        return v;
        }
#endif
    }
#ifdef SINGLE_PRECISION
    __attribute__((aligned(8)));
#else
    __attribute__((aligned(16)));
#endif

//! Computes cosine angle forces on each particle
/*! Cosine angle forces are computed on every particle in the simulation.

    The angles which forces are computed on are accessed from ParticleData::getAngleData
    \ingroup computes
*/
class PYBIND11_EXPORT CosineAngleForceCompute : public ForceCompute
    {
    public:
    //! Constructs the compute
    CosineAngleForceCompute(std::shared_ptr<SystemDefinition> sysdef);

    //! Destructor
    virtual ~CosineAngleForceCompute();

    //! Set the parameters
    virtual void setParams(unsigned int type, Scalar K, Scalar t_0);

    virtual void setParamsPython(std::string type, pybind11::dict params);

    /// Get the parameters for a given type
    virtual pybind11::dict getParams(std::string type);

#ifdef ENABLE_MPI
    //! Get ghost particle fields requested by this pair potential
    /*! \param timestep Current time step
     */
    virtual CommFlags getRequestedCommFlags(uint64_t timestep)
        {
        CommFlags flags = CommFlags(0);
        flags[comm_flag::tag] = 1;
        flags |= ForceCompute::getRequestedCommFlags(timestep);
        return flags;
        }
#endif

    protected:
    Scalar* m_K;   //!< K parameter for multiple angle types
    Scalar* m_t_0; //!< r_0 parameter for multiple angle types

    std::shared_ptr<AngleData> m_angle_data; //!< Angle data to use in computing angles

    //! Actually compute the forces
    virtual void computeForces(uint64_t timestep);
    };

    } // end namespace md
    } // end namespace hoomd

#endif
