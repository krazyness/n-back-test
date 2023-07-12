<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!--[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]--!>



<h3 align="center">N-Back Test</h3>

  <p align="center">
    A program including a 2-Back and 3-Back Test.
    <br />
    <a href="https://github.com/krazyness/n-back-test"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/krazyness/n-back-test">View Demo</a>
    ·
    <a href="https://github.com/krazyness/n-back-test/issues">Report Bug</a>
    ·
    <a href="https://github.com/krazyness/n-back-test/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

There are some good N-Back Tests available online; however, none of them fitted my needs, so I created this N-Back Test that can run as a
stand-alone program that doesn't require network to keep collected data secure.

Here's why you should use my N-Back program:
* It includes a practice round, 2-Back, and 3-Back test
* It saves by a text file you can create
* It provides 4 options that you can change about the test. The amount of trials, the amount of matches in those tests, the number of seconds the
letter will appear, and the interval between each appearing letter. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.com]][Python-url]
* [![PySide6][PySide6.com]][PySide6-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy running, here's how you can install it!

### Prerequisites

_Here's a list of things you need for the program._

**If you're going to install the repo:**
* Python Library
* PySide6

**If you're going to install the EXE:**
* Windows

### Installation

_Here's how you're going to install the program._

**If you're installing the repo:**
1. Clone the repo
   ```sh
   git clone https://github.com/krazyness/n-back-test.git
   ```

**If you're installing the EXE:**
1. Download the latest release from https://github.com/krazyness/n-back-test/releases
2. Extract 'n-back.zip' into the C: Drive

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

_Here's how you can use the program._

**If you installed with the repo:**
1. Pick/create a directory to place the test results in. During the N-Back test, it's going to require you to make a .txt file so that the
program can place test results there.
2. Run the N-Back test
   ```sh
   python /where_you_cloned_the_repo_to/n-back.py
   ```
3. (Optional) Adjust settings for the N-Back Test
   ```sh
   python /where_you_cloned_the_repo_to/n-back.py --trials 25 --matches 7 --letter-duration 0.75 --pause 2
   ``` 
The number after "--trials" correlates to the number of trials in the n-back tests.

The number after "--matches" correlates to the minimum number of n-back matches in each test.

The number after "--letter-duration" correlates to the amount of time (in seconds) the letter will appear during the n-back test.

The number after "--pause" correlates to the interval (in seconds) between each letter appearing.

**You may adjust those numbers to your liking.**


**If you installed the EXE:**
1. Pick/create a directory to place the test results in. During the N-Back test, it's going to require you to make a .txt file so that the
program can place test results there.
2. Go to the unzipped folder named `n-back` under the C: Drive.
3. Run the shortcut named `Click me to run`, and it should run the full N-Back test.
4. (Optional) Adjust settings for the N-Back Test by right-clicking on `Click me to run`, and going into its properties. You can adjust the
settings of the N-Back Test under "Target".

![4dc27c87-3c94-41d8-991b-2b9adaa3c50e](https://github.com/krazyness/n-back-test/assets/138156236/f0b3989d-f91e-4422-91e7-514ff4819582)

The text under "Target" should say "C:\n-back\n-back.exe --trials 25 --matches 7 --letter-duration 0.75 --pause 2"

The number after "--trials" correlates to the number of trials in the n-back tests.

The number after "--matches" correlates to the minimum number of n-back matches in each test.

The number after "--letter-duration" correlates to the amount of time (in seconds) the letter will appear during the n-back test.

The number after "--pause" correlates to the interval (in seconds) between each letter appearing.

**You may adjust those numbers to your liking.**

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
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



<!-- LICENSE -->
## License

Distributed under the MIT License. See `n-back.py` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Brody Dai - brodyxdai@gmail.com - Discord: dudethatskrazy

Project Link: [https://github.com/krazyness/n-back-test](https://github.com/krazyness/n-back-test)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best README Template](https://github.com/othneildrew/Best-README-Template)
* [Image Shields](https://shields.io/)
* [Choose an Open Source License](https://choosealicense.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!--[contributors-shield]: https://img.shields.io/github/contributors/krazyness/n-back-test.svg?style=for-the-badge
[contributors-url]: https://github.com/krazyness/n-back-test/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/krazyness/n-back-test.svg?style=for-the-badge
[issues-url]: https://github.com/krazyness/n-back-test/issues
[license-shield]: https://img.shields.io/github/license/krazyness/n-back-test.svg?style=for-the-badge
[license-url]: https://github.com/krazyness/n-back-test/blob/master/n-back.py-->
[Python.com]: https://img.shields.io/badge/Python-yellow?style=for-the-badge&logo=python&color=ffde50
[Python-url]: https://www.python.org/
[PySide6.com]: https://img.shields.io/badge/PySide6-green?style=for-the-badge&logo=qt&color=89e093
[PySide6-url]: https://pypi.org/project/PySide6/
