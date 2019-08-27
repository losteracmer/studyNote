# Fork/Join

> 从java1.7开始推出的并发框架，虽说是Fork，但是其实创建的还是线程，java没有进程(:

## 实例

```java
public class AccumulatorRecursiveTask extends RecursiveTask<Integer> {

    private final int start;

    private final int end;

    private final int[] data;

    private final int LIMIT = 3;

    public AccumulatorRecursiveTask(int start, int end, int[] data) {
        this.start = start;
        this.end = end;
        this.data = data;
    }


    @Override
    protected Integer compute() {
        if ((end - start) <= LIMIT) {
            int result = 0;
            for (int i = start; i < end; i++) {
                result += data[i];
            }
            return result;
        }

        int mid = (start + end) / 2;
        AccumulatorRecursiveTask left = new AccumulatorRecursiveTask(start, mid, data);
        AccumulatorRecursiveTask right = new AccumulatorRecursiveTask(mid, end, data);
        left.fork();
        right.fork();
        //Integer rightResult = right.compute();
        Integer rightResult = right.join();
        Integer leftResult = left.join();

        return rightResult + leftResult;
    }
}

```

这是最简单最暴力的利用ForkJoin框架，当然还可以更加优雅一点，如下

```java
public class ForkJoinCalculator implements Calculator {
    private ForkJoinPool pool;
 
    private static class SumTask extends RecursiveTask<Long> {
        private long[] numbers;
        private int from;
        private int to;
 
        public SumTask(long[] numbers, int from, int to) {
            this.numbers = numbers;
            this.from = from;
            this.to = to;
        }
 
        @Override
        protected Long compute() {
            // 当需要计算的数字小于6时，直接计算结果
            if (to - from < 6) {
                long total = 0;
                for (int i = from; i <= to; i++) {
                    total += numbers[i];
                }
                return total;
            // 否则，把任务一分为二，递归计算
            } else {
                int middle = (from + to) / 2;
                SumTask taskLeft = new SumTask(numbers, from, middle);
                SumTask taskRight = new SumTask(numbers, middle+1, to);
                taskLeft.fork();
                taskRight.fork();
                return taskLeft.join() + taskRight.join();
            }
        }
    }
 
    public ForkJoinCalculator() {
        // 也可以使用公用的 ForkJoinPool：
        // pool = ForkJoinPool.commonPool()
        pool = new ForkJoinPool();
    }
 
    @Override
    public long sumUp(long[] numbers) {
        return pool.invoke(new SumTask(numbers, 0, numbers.length-1));
    }
}
//这段代码采用了ForkJoin线程池，在效率上可能更加高一些，就像我们推荐使用ExecutorService而不是自己去new线程一样
```

可以看出很想归并的思想，对任务进行拆分，知道达到一个足够小的范围，这里是小于等于3为止。采用多个线程并行执行计算每一段的结果，再将所得到的的结果加起来一步步网上递归回去，计算得到最终结果；

伪代码：

```java
if (这个任务足够小){ 
  执行要做的任务 
} else { 
  将任务分割成两小部分 
  执行两小部分并等待执行结果 
}  
```



## 原理

- `fork()`：开启一个新线程（或是重用线程池内的空闲线程），将任务交给该线程处理。
- `join()`：等待该任务的处理线程处理完毕，获得返回值。

但是问题就是，你如何能保证用多少个线程才能最高效的完成所有细化出来的任务，难道就是疯狂的开启线程，或者利用线程池的思想，将所有的任务放入任务队列中？其实原理和这个很相似，但也有不同的地方。

```java
pool.getPoolSize()
```

执行上面的代码，	你就可以看到到底有多少个任务正在被执行。这里我盲猜应该是和你的机器CPU核心数相差无几

事实上，Fork/Join Framework 的实现是一个复杂的算法——这个算法的名字就叫做 *work stealing*（偷窃） 算法。



- `ForkJoinPool` 的每个工作线程都维护着一个**工作队列**（`WorkQueue`），这是一个双端队列（Deque），里面存放的对象是**任务**（`ForkJoinTask`）。
- 每个工作线程在运行中产生新的任务（通常是因为调用了 `fork()`）时，会放入工作队列的队尾，并且工作线程在处理自己的工作队列时，使用的是 *LIFO* 方式，也就是说每次从队尾取出任务来执行。
- 每个工作线程在处理自己的工作队列同时，会尝试**窃取**一个任务（或是来自于刚刚提交到 pool 的任务，或是来自于其他工作线程的工作队列），窃取的任务位于其他线程的工作队列的队首，也就是说工作线程在窃取其他工作线程的任务时，使用的是 *FIFO* 方式。
- 在遇到 `join()` 时，如果需要 join 的任务尚未完成，则会先处理其他任务，并等待其完成。
- 在既没有自己的任务，也没有可以窃取的任务时，进入休眠。

这里是[并发编程网摘取的一段内容](http://ifeve.com/java-fork-join-framework/)

- 每一个工作线程维护自己的调度队列中的可运行任务。
- 队列以双端队列的形式被维护（注：`deques`通常读作『decks』），不仅支持后进先出 —— `LIFO`的`push`和`pop`操作，还支持先进先出 —— `FIFO`的`take`操作。
- 对于一个给定的工作线程来说，任务所产生的子任务将会被放入到工作者自己的双端队列中。
- 工作线程使用后进先出 —— `LIFO`（最新的元素优先）的顺序，通过弹出任务来处理队列中的任务。
- 当一个工作线程的本地没有任务去运行的时候，它将使用先进先出 —— `FIFO`的规则尝试随机的从别的工作线程中拿（『窃取』）一个任务去运行。
- 当一个工作线程触及了`join`操作，如果可能的话它将处理其他任务，直到目标任务被告知已经结束（通过`isDone`方法）。所有的任务都会无阻塞的完成。
- 当一个工作线程无法再从其他线程中获取任务和失败处理的时候，它就会退出（通过`yield`、`sleep`和/或者优先级调整）并经过一段时间之后再度尝试直到所有的工作线程都被告知他们都处于空闲的状态。在这种情况下，他们都会阻塞直到其他的任务再度被上层调用。

## 细节



下面来介绍一下关键的两个函数：`fork()` 和 `join()` 的实现细节，相比来说 `fork()` 比 `join()` 简单很多，所以先来介绍 `fork()`。

### fork

`fork()` 做的工作只有一件事，既是**把任务推入当前工作线程的工作队列里**。可以参看以下的源代码：

```java
public final ForkJoinTask<V> fork() {
    Thread t;
    if ((t = Thread.currentThread()) instanceof ForkJoinWorkerThread)
        ((ForkJoinWorkerThread)t).workQueue.push(this);
    else
        ForkJoinPool.common.externalPush(this);
    return this;
}
```

### join

`join()` 的工作则复杂得多，也是 `join()` 可以使得线程免于被阻塞的原因——不像同名的 `Thread.join()`。

1. 检查调用 `join()` 的线程是否是 ForkJoinThread 线程。如果不是（例如 main 线程），则阻塞当前线程，等待任务完成。如果是，则不阻塞。
2. 查看任务的完成状态，如果已经完成，直接返回结果。
3. 如果任务尚未完成，但处于自己的工作队列内，则完成它。
4. 如果任务已经被其他的工作线程偷走，则窃取这个小偷的工作队列内的任务（以 *FIFO* 方式），执行，以期帮助它早日完成欲 join 的任务。
5. 如果偷走任务的小偷也已经把自己的任务全部做完，正在等待需要 join 的任务时，则找到小偷的小偷，帮助它完成它的任务。
6. 递归地执行第5步。

> 你偷我的，让我无活可干，我就以牙还牙，敌人的敌人，还是敌人，递归偷，不到饥荒永不休。

