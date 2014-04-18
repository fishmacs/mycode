class Roulette
  # def method_missing(name, *args)
  #   person = name.to_s.capitalize
  #   number = 0
  #   3.times do
  #     number = rand(10) + 1
  #     puts "#{number}..."
  #   end
  #   "#{person} got a #{number}"
  # end
  
  def func()
    3.times do
      number = rand(10) + 1
      puts "#{number}..."
    end
  end
end

class String
  def method_missing(method, *args)
    method == :ghost_reverse ? reverse : super
  end
end

require 'benchmark'

Benchmark.bm do |b|
  b.report 'Normal method' do
    1000000.times { "abc".reverse }
  end
  b.report 'Ghost method' do
    1000000.times { "abc".ghost_reverse }
  end
end
