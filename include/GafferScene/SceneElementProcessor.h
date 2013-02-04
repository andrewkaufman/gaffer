//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2012, John Haddon. All rights reserved.
//  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#ifndef GAFFERSCENE_SCENEELEMENTPROCESSOR_H
#define GAFFERSCENE_SCENEELEMENTPROCESSOR_H

#include "GafferScene/SceneProcessor.h"

namespace GafferScene
{

/// The SceneElementProcessor class provides a base class for modifying elements of an input
/// scene while leaving the scene hierarchy unchanged.
class SceneElementProcessor : public SceneProcessor
{

	public :

		SceneElementProcessor( const std::string &name=staticTypeName() );
		virtual ~SceneElementProcessor();

		IE_CORE_DECLARERUNTIMETYPEDEXTENSION( SceneElementProcessor, SceneElementProcessorTypeId, SceneProcessor );
		
		Gaffer::IntPlug *filterPlug();
		const Gaffer::IntPlug *filterPlug() const;
		
		/// Implemented so that each child of inPlug() affects the corresponding child of outPlug()
		virtual void affects( const Gaffer::ValuePlug *input, AffectedPlugsContainer &outputs ) const;
				
	protected :

		/// Implemented to prevent non-Filter nodes being connected to the filter plug.
		virtual bool acceptsInput( const Gaffer::Plug *plug, const Gaffer::Plug *inputPlug ) const;

		/// Implemented to call hash*() where appropriate - derived classes should implement those methods
		/// rather than this one.
		virtual void hash( const Gaffer::ValuePlug *output, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		
		/// Implemented to call processBound() where appropriate.
		virtual Imath::Box3f computeBound( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const;
		/// Implemented to call processTransform() where appropriate.
		virtual Imath::M44f computeTransform( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const;
		/// Implemented to call processAttributes() where appropriate.
		virtual IECore::ConstCompoundObjectPtr computeAttributes( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const;
		/// Implemented to call processObject() where appropriate.
		virtual IECore::ConstObjectPtr computeObject( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const;
		/// Implemented as a pass-through.
		virtual IECore::ConstInternedStringVectorDataPtr computeChildNames( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const;
		/// Implemented as a pass-through.
		virtual IECore::ConstObjectVectorPtr computeGlobals( const Gaffer::Context *context, const ScenePlug *parent ) const;
		
		/// @name Scene processing methods
		/// These methods should be reimplemented by derived classes to process the input scene - they will be called as
		/// appropriate based on the result of the filter applied to the node. To process a particular
		/// aspect of the scene you must reimplement processesAspect() to return true, reimplement
		/// hashAspect() to append to the hash appropriately (the path will already have been appended),
		/// and finally reimplement the processAspect() function to perform the processing.
		/////////////////////////////////////////////////////////////////////////////////////////////////	
		//@{
		virtual bool processesBound() const;
		virtual void hashBound( const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual Imath::Box3f processBound( const ScenePath &path, const Gaffer::Context *context, const Imath::Box3f &inputBound ) const;
		
		virtual bool processesTransform() const;
		virtual void hashTransform( const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual Imath::M44f processTransform( const ScenePath &path, const Gaffer::Context *context, const Imath::M44f &inputTransform ) const;

		virtual bool processesAttributes() const;
		virtual void hashAttributes( const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstCompoundObjectPtr processAttributes( const ScenePath &path, const Gaffer::Context *context, IECore::ConstCompoundObjectPtr inputAttributes ) const;
		
		virtual bool processesObject() const;
		virtual void hashObject( const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstObjectPtr processObject( const ScenePath &path, const Gaffer::Context *context, IECore::ConstObjectPtr inputObject ) const;
		//@}

	private :
	
		static size_t g_firstPlugIndex;
	
};

} // namespace GafferScene

#endif // GAFFERSCENE_SCENEELEMENTPROCESSOR_H
