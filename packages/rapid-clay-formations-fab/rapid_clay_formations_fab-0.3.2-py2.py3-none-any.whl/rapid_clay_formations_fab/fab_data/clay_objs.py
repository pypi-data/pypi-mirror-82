"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import re
from copy import deepcopy
from itertools import count

from compas.datastructures import Mesh as cg_Mesh
from compas.geometry import Frame
from compas.geometry import Translation
from compas_fab.robots import JointTrajectory
from compas_ghpython.artists import MeshArtist

from rapid_clay_formations_fab.robots import reversed_trajectories
from rapid_clay_formations_fab.utils import wrap_list


class ClayBullet(object):
    r"""Describes a clay cylinder.

    Parameters
    ----------
    location : :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Frame`
        Bottom centroid frame of clay volume.
    travel_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing motion between picking egress and
        placing egress.
    place_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing place motion.
    return_travel_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing motion between placing and picking.
    return_place_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing return motion from last compression motion to placing egress.
    bullet_id : :class:`int`, optional
        Unique identifier.
    radius : :class:`float`, optional
        The radius of the initial cylinder.
    height : :class:`float`, optional
        The height of the initial cylinder.
    compression_ratio : :class:`float` (>0, <=1), optional
        The compression height ratio applied to the initial cylinder.
    clay_density : :class:`float`, optional
        Density of clay in g/mm\ :sup:`3`
    cycle_time : :class:`float`, optional
        Cycle time from pick to place and back.
    placed : :obj:`bool`, optional
        If fabrication element has been placed or not.
    time_placed : :obj:`int`, optional
        Time in epoch (seconds from 1970) of fabrication element placement.
    attrs : :obj:`dict`, optional
        Any other attributes needed.
    kwargs : :class:`dict`, optional
        Keyword arguments added as key-value pair to `attrs` and replaces value
        if key already present.
    """  # noqa: E501

    # creates id-s for objects
    _ids = count(0)

    def __init__(
        self,
        location,
        radius=45,
        height=100,
        compression_ratio=0.5,
        egress_frame_distance=200,
        travel_trajectories=None,
        place_trajectories=None,
        return_travel_trajectories=None,
        return_place_trajectories=None,
        bullet_id=None,
        clay_density=2.0,
        cycle_time=None,
        placed=False,
        time_placed=None,
        attrs=None,
        **kwargs
    ):
        if not isinstance(location, Frame):
            raise Exception("Location should be given as a compas.geometry.Frame")
        self.location = location

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.egress_frame_distance = egress_frame_distance

        self.travel_trajectories = travel_trajectories
        self.place_trajectories = place_trajectories
        self.return_travel_trajectories = return_travel_trajectories
        self.return_place_trajectories = return_place_trajectories

        # sortable ID, used for fabrication sequence
        if not bullet_id:
            self.bullet_id = next(self._ids)
        else:
            self.bullet_id = bullet_id

        self.clay_density = clay_density

        self.cycle_time = cycle_time
        self.placed = placed
        self.time_placed = time_placed

        self.attrs = attrs or {}
        self.attrs.update(kwargs)

    @property
    def return_travel_trajectories(self):
        return self.return_travel_trajectories_ or reversed_trajectories(
            self.travel_trajectories
        )

    @return_travel_trajectories.setter
    def return_travel_trajectories(self, trajectories):
        self.return_travel_trajectories_ = trajectories

    @property
    def return_place_trajectories(self):
        return self.return_place_trajectories_ or reversed_trajectories(
            self.place_trajectories
        )

    @return_place_trajectories.setter
    def return_place_trajectories(self, trajectories):
        self.return_place_trajectories_ = trajectories

    def get_location_plane(self):
        """Get location as Rhino.Geometry.Plane.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        from rapid_clay_formations_fab.rhino import cgframe_to_rgplane

        return cgframe_to_rgplane(self.location)

    def get_normal(self):
        """Get normal direction of cylinder.

        Actually the reverse of the location frame's normal as it's used as a
        robot target frame and thus pointing "down".

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.location.normal * -1

    def get_uncompressed_top_frame(self):
        """Top of uncompressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.height
        T = Translation(vector)

        return self.location.transformed(T)

    def get_compressed_top_frame(self):
        """Top of compressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.get_compressed_height()
        T = Translation(vector)

        return self.location.transformed(T)

    def get_egress_frame(self):
        """Get Frame at end and start of trajectory to and from.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.egress_frame_distance
        T = Translation(vector)

        return self.get_uncompressed_top_frame().transformed(T)

    def get_uncompressed_centroid_frame(self):
        """Get frame at middle of uncompressed bullet.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.height / 2
        T = Translation(vector)

        return self.location.transformed(T)

    def get_compressed_centroid_frame(self):
        """Get frame at middle of compressed bullet.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.get_compressed_height() / 2
        T = Translation(vector)

        return self.location.transformed(T)

    def get_volume(self):
        r"""Get volume of clay bullet in mm\ :sup:`3`\ .

        Returns
        -------
        :obj:`float`
        """
        return math.pi * self.radius ** 2 * self.height

    def get_volume_m3(self):
        r"""Get volume of clay bullet in m\ :sup:`3`\ .

        Returns
        -------
        :obj:`float`
        """
        return self.volume * 1e-9

    def get_weight_kg(self):
        """Get weight of clay bullet in kg.

        Returns
        -------
        :obj:`float`
        """
        return self.density * self.volume * 1e-6

    def get_weight(self):
        """Get weight of clay bullet in g.

        Returns
        -------
        :obj:`float`
        """
        return self.weight_kg * 1000

    def get_compressed_radius(self):
        """Get radius of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        :obj:`float`
        """
        return math.sqrt(self.get_volume() / (self.get_compressed_height() * math.pi))

    def get_compressed_height(self):
        """Get height of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        :obj:`float`
        """
        return self.height * self.compression_ratio

    def get_rgcircle(self):
        """Get :class:`Rhino.Geometry.Circle` representing bullet footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        from Rhino.Geometry import Circle

        return Circle(self.get_location_plane(), self.get_compressed_radius())

    def get_rgcylinder(self):
        """Get :class:`Rhino.Geometry.Cylinder` representing bullet.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        from Rhino.Geometry import Cylinder

        return Cylinder(self.get_rgcircle(), self.get_compressed_height())

    def get_rgvector_from_bullet_zaxis(self):
        """Vector through center of bullet.

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.get_normal() * self.get_compressed_height()

    def copy(self):
        """Get a copy of instance.

        Returns
        -------
        :class:`rapid_clay_formations_fab.fab_data.ClayBullet`
        """
        return deepcopy(self)

    def get_cgmesh(self, face_count=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : :class:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        # TODO: Rewrite as pure compas (unnecessary but neat)
        import Rhino.Geometry as rg

        from rapid_clay_formations_fab.rhino import cgvector_to_rgvector

        if face_count < 6:
            sides = 3
        elif face_count < 15:
            sides = 4
        else:
            sides = face_count // 3

        circle = self.get_rgcircle()

        polygons = []
        polygons.append(rg.Polyline.CreateInscribedPolygon(circle, sides))

        T = rg.Transform.Translation(
            cgvector_to_rgvector(self.get_normal()) * self.get_compressed_height()
        )

        second_polygon = polygons[0].Duplicate()
        second_polygon.Transform(T)

        polygons.append(second_polygon)

        mesh = cg_Mesh()
        outer_verts_polygons = []

        # generate verts at polygon corners
        for polygon in polygons:
            _temp_list = []

            polygon_corners = list(polygon.Item)
            polygon_corners.pop()  # remove end pt since == start pt

            for pt in polygon_corners:
                _temp_list.append(mesh.add_vertex(x=pt.X, y=pt.Y, z=pt.Z))
            outer_verts_polygons.append(_temp_list)

        polygon_faces = []
        for vkeys in outer_verts_polygons:
            polygon_faces.append(mesh.add_face(vkeys))

        # if >4 sides polygon, create faces by tri subd
        if sides > 4:

            centroid_verts = []
            for fkey in polygon_faces:
                x, y, z = mesh.face_centroid(fkey)
                centroid_verts.append(mesh.add_vertex(x=x, y=y, z=z))
                mesh.delete_face(fkey)

            # create new faces
            for vkeys, ckey in zip(outer_verts_polygons, centroid_verts):
                for i, vkey in enumerate(vkeys):
                    next_vkey = wrap_list(vkeys, i + 1)
                    mesh.add_face([ckey, vkey, next_vkey])

        # generate faces between polygons
        vertex_for_vertex = zip(*outer_verts_polygons)

        for i, mirror_corners_1 in enumerate(vertex_for_vertex):
            mirror_corners_2 = wrap_list(vertex_for_vertex, i + 1)
            mesh.add_face(mirror_corners_1 + mirror_corners_2[::-1])

        return mesh

    def get_rgmesh(self, face_count=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : :class:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        mesh = self.get_cgmesh(face_count=face_count)
        # to Rhino.Geometry and clean it up
        rgmesh = MeshArtist(mesh).draw_mesh()
        rgmesh.UnifyNormals()
        rgmesh.Normals.ComputeNormals()

        return rgmesh

    def to_data(self):
        """Get :obj:`dict` representation of :class:`ClayBullet`."""
        # TODO: Remove method. #62 blocks.
        # Check if this is at all needed, or can be done just using
        # CompasObjEncoder
        data = {}

        for key, value in self.__dict__.items():
            if hasattr(value, "to_data"):
                data[key] = value.to_data()
            else:
                data[key] = value

        return data

    @classmethod
    def from_data(cls, data):
        """Construct a :class:`ClayBullet` instance from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`ClayBullet`
            The constructed ClayBullet instance
        """

        def trajectory_from_data(traj_data):
            try:
                return JointTrajectory.from_data(traj_data)
            except AttributeError:
                return [Frame.from_data(frame_data) for frame_data in traj_data]

        kwargs = {}

        location = Frame.from_data(data.pop("location"))

        trajectory_attributes = (
            "travel_trajectories",
            "place_trajectories",
            "return_travel_trajectories_",
            "return_place_trajectories_"
        )

        for key in trajectory_attributes:
            trajectories_data = data.pop(key, None)

            if trajectories_data:
                keyword = re.sub(r"_$", "", key)  # Strip underscore from end of key
                trajectories = []
                for traj_data in trajectories_data:
                    trajectories.append(trajectory_from_data(traj_data))

                kwargs[keyword] = trajectories

        # merge kwargs with data
        kwargs.update(data)

        return cls(location, **kwargs)


def check_id_collision(clay_bullets):
    """Check for duplicate ids in list of ClayBullet instances.

    Parameters
    ----------
    clay_bullets : list of :class:`ClayBullet`

    Raises
    ------
    Exception
        Raises exception when first duplicate is found
    """
    ids = [bullet.bullet_id for bullet in clay_bullets]

    set_of_ids = set()
    for id_ in ids:
        if id_ in set_of_ids:
            raise Exception(
                "Id {} appears more than once in list of ClayBullet instances".format(
                    id_
                )
            )
        set_of_ids.add(id_)
