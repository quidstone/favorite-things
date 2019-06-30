
# Questions and Answers

> How long did I spend on the coding test?

Hi guys. When i read the requirements, i found it interesting as well as challenging. you guys have created the most interesting and fun test for me. It was great thinking about the problems and what i can do to solve that. python/vue is kind of familiar to me as i have worked with java/java-spring-webmvc/rest/react. So i just had to do vue a bit and then some flask for this project. i have done some data science projects with python, so python is not new to me. For the exact timing i would say, frontend part was done in 5/6 days with 8 hour office in those 3 days every day and flask/python is for another 3/4 days, ofcourse excluding 8 hrs office times.

> What would you add to your solution if you had more time?

* frontend
  1.i love components and events, i have not done too many split ups. i have made a clumsy project for this test. But i would love more proper components and props/events in between.

  2.i would love header/footer and routes for sure.
  
  3.i would love loaders while api calling.

  4.validation checks

* back-end
  1.structurally i would love proper models and functions in the models, my package structure for the project is okay for the scale of the test. but if it grows then i would have to split it up into modules.

  2.input sanitization is a must to handle the security better. i wouldn't say much about the authentication/authorization as these thing are must but for the test it would be overwhelming.

  3.i havent done the testing for all apis. But i would love to do that. proper testing is always handy and it actually saves.

  4.i wanted to make configuration easy with a .py file but i didn't have time...sorry for that.

  5.i want to wrap all response in a class and consistent fields/keys for json responses. i have done that with http response codes but theres a better way and i know that and i can do that too.

* sql
  1.i wanted to have different items_metadata table with data types column just to establish a relashionship later but for that i would love in memory dbs and later syncing with mysql

>What was the most useful feature that was added to the latest version of your chosen language?

## Splicing for maps and sets

Moving nodes and merging containers without the overhead of expensive copies, moves, or heap allocations/deallocations. I will mention two uses-cases:

* Moving elements from one map to another:

```c++
std::map<int, string> src {{1, "one"}, {2, "two"}, {3, "buckle my shoe"}};
std::map<int, string> dst {{3, "three"}};
dst.insert(src.extract(src.find(1))); // Cheap remove and insert of { 1, "one" } from `src` to `dst`.
dst.insert(src.extract(2)); // Cheap remove and insert of { 2, "two" } from `src` to `dst`.
// dst == { { 1, "one" }, { 2, "two" }, { 3, "three" } };
```

* Inserting an entire set:

```c++
std::set<int> src {1, 3, 5};
std::set<int> dst {2, 4, 5};
dst.merge(src);
// src == { 5 }
// dst == { 1, 2, 3, 4, 5 }
```

> How would you track down a performance issue in production?

i have worked with c/c++ projects which consumes/delivers hume amount of network packets. so achieving performance is not new to me. i am quite familiar with threads,stacks,queues meaning runtime/memory stuffs but i am also learning to achieve the seet spot between the trade-offs. so i think i can handle performance issues. for web services/web servers i would try to scale the servers and instances for better load-balancing. and i want to know about distributed resource handling/distributed computing and stuff.

>Have you ever had to do this?

* we had a scenario where deadlock on queries happened frequently, and we had to find the perfect index for the db tables

* we made a system multi-threaded just to better the packet transfer rate for an IVR system and a protocol translator.

* we stopped memory leaking in a c++ application by implementing unique_ptrs and buffer overflows using address sanitization
