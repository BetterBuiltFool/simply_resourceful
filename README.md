<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!--
[![LinkedIn][linkedin-shield]][linkedin-url]
-->



<!-- PROJECT LOGO -->
<br />
<!--
<div align="center">
  <a href="https://github.com/BetterBuiltFool/simply_resourceful">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">Simply Resourceful</h3>

  <p align="center">
    The Simple Resource Manager
    <br />
    <a href="https://github.com/BetterBuiltFool/simply_resourceful"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!--
    <a href="https://github.com/BetterBuiltFool/simply_resourceful">View Demo</a>
    ·
    -->
    <a href="https://github.com/BetterBuiltFool/simply_resourceful/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/BetterBuiltFool/simply_resourceful/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#types">Types</a></li>
        <li><a href="#using-asset-handles">Using Asset Handles</a></li>
        <li><a href="#importing-resources">Importing Resources</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <!--<li><a href="#contributing">Contributing</a></li>-->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

Simply Resourceful is a simple resource manager, designed to work alongside pygame. It offers deferred loading of resources, as well as a simple way of accessing those resources in your code, making swapping out resources a breeze.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Simply Resourceful is written in pure python, with no system dependencies, and should be OS-agnostic.

### Installation

Simply Resourceful can be installed from the [PyPI][pypi-url] using [pip][pip-url]:

```sh
pip install simply_resourceful
```

and can be imported for use with:
```python
import resourceful
```

Simply Resourceful has no mandatory dependencies, but has some extra options when Pygame Community Edition is installed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Assets can often be a heavy burden on memory. The process of loading them from file or downloading them can also be intensive. Having your assets loaded only once, and then reused whenever needed, can help reduce the load. Additionally, instead of loading all assets immediatly, lazy loading allows the load times to be deferred until an asset is needed, and never coming into memory at all if never requested.

Resource Managers are created with 
```python
import resourceful

MANAGER = resourceful.getResourceManager(<type>, "handle")
```

Where ```<type>``` is the class of resource to be managed.

This will ensure that a resource manager for the given type and of the given handle exists.
Handles are optional, but are useful for having resource managers with different loading behavior despite the same resource type, without increasing the complexity of the loader function.

Note that for the rest of the document, 'resource' and 'asset' may be used interchangeably.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Preconfigured Managers

Additionally, if you have pygame-ce installed, you also gain eccess to two additional methods, resourceful.getImageManager() and resourceful.getSoundManager(). These are preconfigured resource managers for loading images and sounds from disk, respectively. They are not tracked by the Resource Manager, and must be gotten with these methods. These prebuilt managers are designed to take file paths for their resource location data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Types

Resource Managers are generic, and can handle almost any type of data. The type you want the resource manager to handle must be specified before use.

```python
import pygame
import resourceful

MANAGER = resourceful.getResourceManager(pygame.Surface)
```

In this example, a resource manager that handles pygame surfaces will be created or found, if it exists, with a blank handle. This might be useful for storing images loaded into memory in one single place.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Using Asset Handles

Resources are referenced by asset handles, which are strings that ascribe common names to their resources. They are used as such:
```python

sprite.image = image_manager.get("Hero")
```

This will check the manager for an asset called "Hero", load it if necessary, and supply the sprite with it for display.

In more complicated use cases, it may be desirable to supply a default value. This may be because the asset handle being requested is coming from elsewhere, and might not be guaranteed to be correct, and something is needed to fill the gap.

That use case would look something like this:
```python

sprite.image = image_manager.get(current_hero_pose, hero_blank_sprite)
```

This way, if current_hero_pose accidentally refers to an invalid resource, the program will not crash.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Importing Resources

Before any assets are requested, the resource manager must be made aware of the assets it will manage. This must be done early on in the program, before any manager.get() operations are called.
```python
# ---Program set up stuff---
# Global variables and such, module initialization, whatever.
manager.import_asset("Hero", "path/to/hero.png")
```

In this example, the manager now is aware of an asset called "Hero", as well as a path to find it for loading.

Location data can be anything the loader function can use to generate the asset. Typically, it will be a file location, but could also be a tuple of draw data for drawing surfaces, or data for downloading an asset from a database, or anything else, really.

Assets can also be force-loaded, which is similar to importing, but loads the asset into memory from its location data immediately, no need to have something call get(). This might be useful for assets that are guaranteed to be used immediately.

#### Mass Import

Alternatively, you may also perform a mass import, using
```python
manager.import_directory("path/to/asset/folder")
```

This will import everything from the given directory. It has additional options, such as searching subfolders, and filter functions to change filtering, naming, and location data generation. This provides an easier to use way to import many assets, at the cost of control.

By default, import_directory will import all files regardless of file type, names them based on their file name (and subfolder, if enabled), and gives their file path as their location data.

#### Resource File

It may be advisable to keep a separate module that contains all of your asset imports. This will collect them all in one place, outside of your main program code.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Configuration

#### Loader Functions

Because resource managers are generic, they have no inherent knowledge of how to load any given resource. So, a loader function must be supplied.
For example:
```python
def image_loader(resource_location: Path | str) -> pygame.Surface:
    asset = pygame.image.load(resource_location)
    return asset.convert()

# ---Program set up stuff---
# Global variables and such, module initialization, whatever.
manager.config(loader_helper=image_loader)
manager.import_asset("Hero", "path/to/hero.png")
```

This will load the image from the path, and convert it to be ready for use.

Loader functions only have two requirements:
1. They must take the same data as is used for location data by the resource manager. That is, if the location data is a path, the loader must take a path.
2. They must return the same type as the resource manager, or None, indicating a load failure.
They can do anything else you'd like, and can be a simple or as complicated as you want. to extend the above example, you could have it check the file extension to determine if convert() is sufficient, or if convert_alpha() would be preferable.

Additionally, in an async-aware environment, you could have your loader begin a coroutine to download your asset, and return a default asset to tide things over until then, updating the asset upon completion.

From there, the resource manager will take over, loading and supplying resources as needed by other parts of the program.

#### Default Assets

A default asset may be provided in the config function, allowing suppression of errors for loading failures by always having an option to fill in any blanks. If get() is called with a default value, it will override the manager-level default asset.

None is considered a valid default, and should be handled appropriately. Simply Resourceful makes use of a sentinel value called NoDefault to determine that a default value does not exist or shouldn't be used.

```python
manager.config(default_asset=some_asset)
```

#### Preconfigured Options

With pygame-ce installed, you additionally have access to two preconfigured resource managers, one for images (built around pygame Surfaces), and one for sounds. These both handle loading their respective resources automatically, and require PathLike data for their resource_location data.

<!--
_For more examples, please refer to the [Documentation](https://example.com)_
-->


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Make pickleable for saving and loading resource managers.
- [ ] Allow for objects to request proxies that don't load the asset until it is called upon.
    - This may not be possible for all objects.
- [ ] Make a visual importing tool to generate pickle files for easy imports.

<!--
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature
-->

See the [open issues](https://github.com/BetterBuiltFool/simply_resourceful/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<!--
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/BetterBuiltFool/simply_resourceful/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BetterBuiltFool/simply_resourceful" alt="contrib.rocks image" />
</a>
-->



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Better Built Fool - betterbuiltfool@gmail.com

Bluesky - [@betterbuiltfool.bsky.social](https://bsky.app/profile/betterbuiltfool.bsky.social)
<!--
 - [@twitter_handle](https://twitter.com/twitter_handle)
-->

Project Link: [https://github.com/BetterBuiltFool/simply_resourceful](https://github.com/BetterBuiltFool/simply_resourceful)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!--## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BetterBuiltFool/simply_resourceful.svg?style=for-the-badge
[contributors-url]: https://github.com/BetterBuiltFool/simply_resourceful/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BetterBuiltFool/simply_resourceful.svg?style=for-the-badge
[forks-url]: https://github.com/BetterBuiltFool/simply_resourceful/network/members
[stars-shield]: https://img.shields.io/github/stars/BetterBuiltFool/simply_resourceful.svg?style=for-the-badge
[stars-url]: https://github.com/BetterBuiltFool/simply_resourceful/stargazers
[issues-shield]: https://img.shields.io/github/issues/BetterBuiltFool/simply_resourceful.svg?style=for-the-badge
[issues-url]: https://github.com/BetterBuiltFool/simply_resourceful/issues
[license-shield]: https://img.shields.io/github/license/BetterBuiltFool/simply_resourceful.svg?style=for-the-badge
[license-url]: https://github.com/BetterBuiltFool/simply_resourceful/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[pypi-url]: https://pypi.org/project/simply_resourceful
[pip-url]: https://pip.pypa.io/en/stable/