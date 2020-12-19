# lego-mindstorms-ev3-micropython
This repository include a micropython script for "LEGO MINDSTORMS EV3"

# 1. Overview
The project team consists of six people. I was mainly in charge of the program management.  
We want to sort 9 marbles into the square box separated 9 blocks.  
(We used red and blue and green marbles. We have three mables each color.)

![marbles](https://github.com/chihina/lego-mindstorms-ev3-micropython/blob/master/images/marbles.jpg)

# 2. About program
We used micropython, not block programming of MINDSTORMS.  
By using it, we archied the fine control of a intelligent block.  
We chose the color sensor and interactive servo motor. 

- Color sensor: https://www.lego.com/ja-jp/product/ev3-color-sensor-45506  
- Servo motor: https://www.lego.com/ja-jp/product/ev3-medium-servo-motor-45503  

Accuracies of this sensor and motor are limited, so we need to some ingenuities.  
1. We fixed the light condtion as possible as we can.  
2. We tuned the color and motor parameters which fit enviroment.  
3. We built the system which is less susceptible limited of accuracies about color sensor and motor.  

# 3. Result movie
We archied a high performance sorting. It takes 44 seconds !!  

![sorting gif](https://github.com/chihina/lego-mindstorms-ev3-micropython/blob/master/images/sorting_movie.gif)

# 2. Reference 
If you want to write the same code as me, you can see this documents.  
There are a lot of infomation which help you know about micropython and MINDSTORMS.  

https://legoedu.jp/_pdf/news_20190830.pdf  

## Contacts
If you can know about detail me, you can see my website.

- My home page (Github Pages): https://chihina.github.io/portfolio_english.html  

- Qitta page: https://qiita.com/chi-na  

- Linked in: www.linkedin.com/in/chihiro-nakatani-2060b01a9  
