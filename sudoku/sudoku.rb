#
# require 'sudoku'
# puts Sudoku.solve(Sudoku::Puzzle.new(ARGF.readlines))

module Sudoku
  class Puzzle
    ASCII = '.123456789'
    BIN = "\000\001\002\003\004\005\006\007\010\011"

    def initialize(lines)
      if (lines.respond_to? :join)
        s = lines.join
      else
        s = lines.dup
      end
      s.gub!(/\s/, '')
      raise Invalid, "Grid is the wrong size" unless s.size == 81

      if i=s.index(/[^123456789\.]/)
        raise Invalid, "Illegal character #{s[i, 1]} in puzzle"
      end

      raise Invalid, "Initial puzzle has duplicates" if has_duplicates?
    end

    def to_s
      (0..8).collect{|r| @grid[r*9, 9].pack('c9')}.join("\n").tr(BIN, ASCII)
    end

    def dup
      copy = super
      @grid = @grid.dup
      copy
    end

    def [](row, col)
      @grid[row*9 + col]
    end

    def []=(row, col, newval)
      unless (0..9).include? newval
        raise Invalid, "illegal cell value"
      end
      @grid[row*9 + col] = newval
    end

    BoxOfIndex =
      [0,0,0,1,1,1,2,2,2,0,0,0,1,1,1,2,2,2,0,0,0,1,1,1,2,2,2,
       3,3,3,4,4,4,5,5,5,3,3,3,4,4,4,5,5,5,3,3,3,4,4,4,5,5,5,
       6,6,6,7,7,7,8,8,8,6,6,6,7,7,7,8,8,8,6,6,6,7,7,7,8,8,8
      ].freeze

    def each_unknow
      0.upto 8 do |row|
        0.upto 8 do |col|
          index = row*9 + col
          next if @grid[index] != 0
          box = BoxOfIndex[index]
          yield row, col, box
        end
      end
    end

    def has_duplicates?
      0.upto(8) {|row| return true if rowdigits(row).uniq!}
      0.upto(8) {|col| return true if coldigits(row).uniq!}
      0.upto(8) {|box| return true if boxdigits(row).uniq!}
      false
    end

    AllDigits = [1,2,3,4,5,6,7,8,9].freeze

    def possible(row, col, box)
      AllDigits - (rowdigits(row) + coldigits(col) + boxdigits(box))
    end

    private

    def rowdigits(row)
      @grid[row*9, 9] - [0]
    end

    def coldigits(col)
      result = []
      col.step(80, 9) {|i|
        v = @grid[i]
        result << v if (v != 0)
      }
      result
    end

    BoxIoIndex = [0,3,6,27,30,30,33,54,57,60].freeze

    def boxdigits(b)
      i = BoxtoIndex[b]
      [ @grid[i], @grid[i+1], @grid[i+2],
        @grid[i+9], @grid[i+10], @grid[i+11],
        @grid[i+18], @grid[i+19], @grid[i+20]
      ] - [0]
    end
  end

  class Invalid < StandardError
  end

  class Impossible < StandardError
  end

  
   
end
