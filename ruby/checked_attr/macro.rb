require 'test/unit'

Object.instance_eval do
  def attr_checked(attribute, &validation)
    define_method "#{attribute}=" do |value|
      raise 'Invalid attribute' unless validation.call(value)
      instance_variable_set("@#{attribute}", value)
    end

    define_method "#{attribute}" do
      instance_variable_get("@#{attribute}")
    end
  end
end

class Person
  attr_checked(:age) { |v| v >= 18 }
end

class TestCheckedAttributes < Test::Unit::TestCase
  def setup
    @bob = Person.new
  end

  def test_accept_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
  end

  def test_refuses_invalid_values
    assert_raises RuntimeError, 'Invalid attribute' do
      @bob.age = 17
    end
  end
end
