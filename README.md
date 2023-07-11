1. Pick/create a directory to place the test results in. (When students do the test, they're prompted to make a text file under a directory, where the n-back test will edit to show test results. You may instruct them to put the text file under your chosen directory.)
2. Unzip n-back.zip into the C: Drive.
3. After unzipping, go into the unzipped folder under the C: Drive. The folder should be named "n-back".
4. Run the shortcut named "Click me to run", and it should run the full n-back test.
5. To adjust the settings of the test, right-click on "Click me to run", and go into its properties. You can adjust the settings of the n-back test under "Target".

![4dc27c87-3c94-41d8-991b-2b9adaa3c50e](https://github.com/krazyness/n-back-test/assets/138156236/f0b3989d-f91e-4422-91e7-514ff4819582)

The text under "Target" should say "C:\n-back\n-back.exe --trials 25 --matches 7 --letterduration 0.75 --pause 2"

The number after "--trials" correlates to the number of trials in the n-back tests.

The number after "--matches" correlates to the minimum number of n-back matches in each test.

The number after "--letterduration" correlates to the amount of time (in seconds) the letter will appear during the n-back test.

The number after "--pause" correlates to the interval (in seconds) between each letter appearing.
