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

Simply Resourceful also requires Pygame Community edition to be installed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Assets can often be a heavy burden on memory. The process of loading them from file or downloading them can also be intensives. Having your assets loaded only once, and then reused whenever needed, can help reduce the load. Additionally, instead of loading all assets immediatly, lazy loading allows the load times to be deferred until an asset is needed, and never coming into memory at all if never requested.

Resource Managers are created with 
```python
import resourceful

MANAGER = resourceful.getResourceManager(<type>, "handle")
```

This will ensure that a resource manager for the given type and of the given handle exists.
Handles are optional, but are useful for having resource managers with different loading behavior despite the same resource type.

Note that for the rest of the document, 'resource' and 'asset' may be used interchangeably.

### Types

Resource Managers are generic, and can handle any type of data. The type you want the resource manager to handle must be specified before use.

```python
import pygame
import resourceful

MANAGER = resourceful.getResourceManager(pygame.Surface)
```

In this example, a resource manager that handles pygame surfaces will be created or found, if it exists, with a blank handle. This might be useful for storing images loaded into memory in one single place.

### Using Asset Handles

Resources are referenced by asset handles, which are strings that supply common names to their resources. They are used as such:
```python

sprite.image = image_manager.get("Hero")
```

This will check the manager for an asset called "Hero", load it if necessary, and supply the sprite with it for display.

In more complicated use cases, it may be desirable to supply a default value. This may be because the asset handle being requested is coming from elsewhere, and might not be guaranteed to be correct, and something is needed to fill the gap.

That use case would look something like this:
```python

sprite.image = image_manager.get(current_hero_pose, hero_blank_sprite)
```

This way, if current_hero_pose accidentally refers to an invalid resource, the experience of the player will not be interrupted.

### Preloading

Before any assets are requested, the resource manager must be made aware of the assets it will manage. This must be done early on in the program, before any manager.get() operations are called.
```python
# ---Program set up stuff---
# Global variables and such, module initialization, whatever.
manager.preload("Hero", "path/to/hero.png")
```

In this example, the manager now is aware of an asset called "Hero", as well as a path to find it for loading.

Assets can also be force-loaded, which is similar to preloading, but loads the asset into memory from its location data immediately, no need to have something call get(). This might be useful for assets that are guaranteed to be used immediately.

### Configuration

Because resource managers are generic, they have no inherent knowledge of how to load any given resource. So, a loader function must be supplied.
For example:
```python
def image_loader(resource_location: Path | str) -> pygame.Surface:
    asset = pygame.image.load(resource_location)
    return asset.convert()

# ---Program set up stuff---
# Global variables and such, module initialization, whatever.
manager.config(loader_helper=image_loader)
manager.preload("Hero", "path/to/hero.png")
```

This will load the image from the path, and convert it to be ready for use.

Loader functions only have two requirements:
1. They must take the same data as is used for location data by the resource manager. That is, if the location data is a path, the loader must take a path.
2. They must return the same type as the resource manager, or None.

<!--
_For more examples, please refer to the [Documentation](https://example.com)_
-->


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

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