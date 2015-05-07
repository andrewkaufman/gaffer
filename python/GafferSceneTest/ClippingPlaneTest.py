##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import unittest

import IECore

import GafferTest
import GafferScene
import GafferSceneTest

class ClippingPlaneTest( GafferSceneTest.SceneTestCase ) :

	def test( self ) :

		c = GafferScene.ClippingPlane()
		self.assertSceneValid( c["out"] )

		self.assertEqual( c["out"].bound( "/clippingPlane" ), IECore.Box3f( IECore.V3f( -0.5, -0.5, 0 ), IECore.V3f( 0.5 ) ) )

		g = c["out"]["globals"].getValue()
		s = g["gaffer:sets"]["__clippingPlanes"]
		self.assertEqual( s.value.paths(), [ "/clippingPlane" ] )

	def testDirtyPropagation( self ) :

		c = GafferScene.ClippingPlane()

		dirtied = GafferTest.CapturingSlot( c.plugDirtiedSignal() )
		c["transform"]["translate"]["x"].setValue( 10 )
		self.failUnless( c["out"]["transform"] in [ p[0] for p in dirtied ] )

		dirtied = GafferTest.CapturingSlot( c.plugDirtiedSignal() )
		c["name"].setValue( "yupyup" )
		self.failUnless( c["out"]["childNames"] in [ p[0] for p in dirtied ] )
		self.failUnless( c["out"]["globals"] in [ p[0] for p in dirtied ] )

if __name__ == "__main__":
	unittest.main()