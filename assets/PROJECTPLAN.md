# Project Plan for `Vistagrid`

## Project Title: A Django Powered Photo Editing Application

## Start Date: 25/02/2016

## End Date: 18/03/2016

## Application Overview
*  Vistagrid is a photo editing app that is built on the Django web framework. It sports the following features;
  *  Users can login via Facebook
  *  Users can upload images
  *  Users can edit uploaded images (using filters/ effects) which include;
    *  Cropping
    *  Rolling
    *  Transformations
    *  Rotations/ Flips
    *  Colour Transformations
    *  Image sharpening/ enhancing/ blur
    *  Contours
  *  Users can share images using a public url on Facebook

* Vistagrid makes use of `Pillow`; an actively developed forked implementation of the Python Imaging Library. Most of the image processing is handled by this package.

## Tasks and Deliverables

Task Name | Points
--------- | --------
Create Login View   | 0.5
Create Facebook Login Logic  | 1
Create Image Upload Logic | 1
Create Dashboard View   | 2
Create Models   | 0.5
Create Image Cropping Logic | 2
Create Image Rolling Logic | 4
Create Image Transformation Logic | 2
Create Image Rotations/Flip Logic | 2
Create Colour Transformation Logic | 0.5
Create Image Sharpening Logic | 2
Write Tests | 2
Deploy to Heroku| 2