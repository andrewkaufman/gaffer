##########################################################################
#
#  Copyright (c) 2014, John Haddon. All rights reserved.
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

import imath

import IECore

import Gaffer
import GafferTest
import GafferScene
import GafferSceneTest

class DuplicateTest( GafferSceneTest.SceneTestCase ) :

	def test( self ) :

		s = GafferScene.Sphere()
		d = GafferScene.Duplicate()
		d["in"].setInput( s["out"] )
		d["target"].setValue( "/sphere" )
		d["transform"]["translate"].setValue( imath.V3f( 1, 0, 0 ) )

		self.assertSceneValid( d["out"] )

		self.assertEqual( d["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "sphere", "sphere1" ] ) )
		self.assertPathHashesEqual( s["out"], "/sphere", d["out"], "/sphere" )
		self.assertPathHashesEqual( d["out"], "/sphere", d["out"], "/sphere1", childPlugNamesToIgnore = ( "transform", ) )
		self.assertEqual( d["out"].transform( "/sphere1" ), imath.M44f().translate( imath.V3f( 1, 0, 0 ) ) )

	def testMultipleCopies( self ) :

		s = GafferScene.Sphere()
		d = GafferScene.Duplicate()
		d["in"].setInput( s["out"] )
		d["target"].setValue( "/sphere" )
		d["transform"]["translate"].setValue( imath.V3f( 1, 0, 0 ) )
		d["copies"].setValue( 10 )

		self.assertSceneValid( d["out"] )

		self.assertEqual(
			d["out"].childNames( "/" ),
			IECore.InternedStringVectorData(
				[ "sphere" ] + [ "sphere%d" % x for x in range( 1, 11 ) ]
			)
		)

		for i in range( 1, 11 ) :
			path = "sphere%d" % i
			self.assertPathHashesEqual( d["out"], "/sphere", d["out"], path, childPlugNamesToIgnore = ( "transform", ) )
			self.assertEqual( d["out"].transform( path ), imath.M44f().translate( imath.V3f( 1, 0, 0 ) * i ) )

	def testHierarchy( self ) :

		s = GafferScene.Sphere()
		g = GafferScene.Group()
		g["in"][0].setInput( s["out"] )

		d = GafferScene.Duplicate()
		d["in"].setInput( g["out"] )
		d["target"].setValue( "/group" )

		self.assertSceneValid( d["out"] )
		self.assertPathsEqual( d["out"], "/group", d["out"], "/group1" )
		self.assertPathHashesEqual( d["out"], "/group", d["out"], "/group1", childPlugNamesToIgnore = ( "transform", ) )
		self.assertPathsEqual( d["out"], "/group/sphere", d["out"], "/group1/sphere" )
		self.assertPathHashesEqual( d["out"], "/group/sphere", d["out"], "/group1/sphere" )

	def testInvalidTarget( self ) :

		s = GafferScene.Sphere()
		d = GafferScene.Duplicate()
		d["in"].setInput( s["out"] )
		d["target"].setValue( "/cube" )

		self.assertRaises( RuntimeError, d["out"].childNames, "/" )

	def testNamePlug( self ) :

		s = GafferScene.Sphere()
		g = GafferScene.Group()
		g["in"][0].setInput( s["out"] )

		d = GafferScene.Duplicate()
		d["in"].setInput( g["out"] )
		d["target"].setValue( "/group/sphere" )

		for target, name, copies, childNames in [

			( "sphere", "", 1, [ "sphere", "sphere1" ] ),
			( "sphere", "", 2, [ "sphere", "sphere1", "sphere2" ] ),
			( "sphere", "copy", 2, [ "sphere", "copy1", "copy2" ] ),
			( "sphere", "copy", 1, [ "sphere", "copy" ] ),
			( "sphere", "sphere", 1, [ "sphere", "sphere1" ] ),
			( "sphere", "sphere", 2, [ "sphere", "sphere1", "sphere2" ] ),
			( "sphere", "copy10", 2, [ "sphere", "copy10", "copy11" ] ),
			( "sphere", "copy10", 1, [ "sphere", "copy10" ] ),
			( "sphere1", "copy10", 1, [ "sphere1", "copy10" ] ),
			( "sphere1", "sphere10", 1, [ "sphere1", "sphere10" ] ),
			( "sphere1", "sphere10", 2, [ "sphere1", "sphere10", "sphere11" ] ),
			( "sphere12", "sphere10", 1, [ "sphere12", "sphere10" ] ),
			( "sphere12", "sphere10", 2, [ "sphere12", "sphere10", "sphere11" ] ),
			( "sphere12", "sphere11", 2, [ "sphere12", "sphere11", "sphere13" ] ),
			( "sphere12", "copy", 1, [ "sphere12", "copy" ] ),
			( "sphere12", "copy2", 1, [ "sphere12", "copy2" ] ),
			( "sphere12", "copy2", 2, [ "sphere12", "copy2", "copy3" ] ),
			( "sphere12", "sphere12", 1, [ "sphere12", "sphere13" ] ),
			( "sphere12", "sphere12", 2, [ "sphere12", "sphere13", "sphere14" ] ),
		] :

			s["name"].setValue( target )
			d["target"].setValue( "/group/" + target )
			d["name"].setValue( name )
			d["copies"].setValue( copies )

			self.assertSceneValid( d["out"] )
			self.assertEqual( d["out"].childNames( "/group" ), IECore.InternedStringVectorData( childNames ) )

	def testNamePlugAffects( self ) :

		d = GafferScene.Duplicate()
		cs = GafferTest.CapturingSlot( d.plugDirtiedSignal() )

		d["name"].setValue( "test" )
		self.assertTrue( d["out"]["childNames"] in [ c[0] for c in cs ] )

	def testSets( self ) :

		s = GafferScene.Sphere()
		s["sets"].setValue( "set" )

		g = GafferScene.Group()
		g["in"][0].setInput( s["out"] )

		d = GafferScene.Duplicate()
		d["in"].setInput( g["out"] )
		d["target"].setValue( "/group" )
		d["copies"].setValue( 5 )

		self.assertEqual(
			set( d["out"].set( "set" ).value.paths() ),
			set(
				[ "/group/sphere" ] +
				[ "/group%d/sphere" % n for n in range( 1, 6 ) ]
			)
		)

		d["target"].setValue( "/group/sphere" )
		d["copies"].setValue( 1500 )

		self.assertEqual(
			set( d["out"].set( "set" ).value.paths() ),
			set(
				[ "/group/sphere" ] +
				[ "/group/sphere%d" % n for n in range( 1, 1501 ) ]
			)
		)

	def testSetNames( self ) :

		s = GafferScene.Sphere()
		s["sets"].setValue( "testSet" )
		d = GafferScene.Duplicate()
		d["in"].setInput( s["out"] )
		d["target"].setValue( "/sphere" )
		d["transform"]["translate"].setValue( imath.V3f( 1, 0, 0 ) )

		with Gaffer.PerformanceMonitor() as m :
			self.assertEqual( s["out"]["setNames"].hash(), d["out"]["setNames"].hash() )
			self.assertTrue( s["out"]["setNames"].getValue( _copy = False ).isSame( d["out"]["setNames"].getValue( _copy = False ) ) )
			self.assertEqual( s["out"]["setNames"].getValue(), IECore.InternedStringVectorData( [ "testSet" ] ) )

		self.assertEqual( m.plugStatistics( d["out"]["setNames"] ).hashCount, 0 )
		self.assertEqual( m.plugStatistics( d["out"]["setNames"] ).computeCount, 0 )

if __name__ == "__main__":
	unittest.main()
