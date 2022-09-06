# Innodb如何避免幻读

[MySQL的InnoDB的幻读问题](http://blog.sina.com.cn/s/blog_499740cb0100ugs7.html)

> 结论：MySQL InnoDB的可重复读并不保证避免幻读，需要应用使用加锁读来保证。而这个加锁度使用到的机制就是next-key locks。

