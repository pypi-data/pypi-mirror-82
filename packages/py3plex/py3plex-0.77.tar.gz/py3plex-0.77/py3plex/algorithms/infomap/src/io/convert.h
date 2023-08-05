/**********************************************************************************

 Infomap software package for multi-level network clustering

 Copyright (c) 2013, 2014 Daniel Edler, Martin Rosvall
 
 For more information, see <http://www.mapequation.org>
 

 This file is part of Infomap software package.

 Infomap software package is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Infomap software package is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Infomap software package.  If not, see <http://www.gnu.org/licenses/>.

**********************************************************************************/


#ifndef CONVERT_H_
#define CONVERT_H_

#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

#ifdef NS_INFOMAP
namespace infomap
{
#endif

class AbortAndHelp : public std::runtime_error {
public:
	AbortAndHelp(std::string const& s) : std::runtime_error(s) { }
};

class InputSyntaxError : public std::runtime_error {
public:
	InputSyntaxError(std::string const& s) : std::runtime_error(s) { }
};

class UnknownFileTypeError : public std::runtime_error {
public:
	UnknownFileTypeError(std::string const& s) : std::runtime_error(s) { }
};

class FileFormatError : public std::runtime_error {
public:
	FileFormatError(std::string const& s) : std::runtime_error(s) { }
};

class InputDomainError : public std::runtime_error {
public:
	InputDomainError(std::string const& s) : std::runtime_error(s) { }
};

class BadConversionError : public std::runtime_error {
public:
	BadConversionError(std::string const& s) : std::runtime_error(s) { }
};

class MisMatchError : public std::runtime_error {
public:
	MisMatchError(std::string const& s) : std::runtime_error(s) { }
};

class InternalOrderError : public std::logic_error {
public:
	InternalOrderError(std::string const& s) : std::logic_error(s) { }
};

struct ImplementationError : public std::runtime_error {
	ImplementationError(std::string const& s) : std::runtime_error(s) {}
};

template<typename T>
struct TypeInfo {
	static std::string type() { return "undefined"; }
	static bool isNumeric() { return false; }
};
template<>
struct TypeInfo<bool> {
	static std::string type() { return "bool"; }
	static bool isNumeric() { return false; }
};
template<>
struct TypeInfo<int> {
	static std::string type() { return "int"; }
	static bool isNumeric() { return true; }
};
template<>
struct TypeInfo<unsigned int> {
	static std::string type() { return "unsigned int"; }
	static bool isNumeric() { return true; }
};
template<>
struct TypeInfo<double> {
	static std::string type() { return "double"; }
	static bool isNumeric() { return true; }
};


namespace io
{

template<typename T>
inline std::string stringify(T x)
{
	std::ostringstream o;
	if (!(o << x))
		throw BadConversionError((o << "stringify(" << x << ")", o.str()));
	return o.str();
}


template<typename Container>
inline std::string stringify(const Container& cont, std::string delimiter)
{
	std::ostringstream o;
	if (cont.empty())
		return "";
	unsigned int maxIndex = cont.size() - 1;
	for (unsigned int i = 0; i < maxIndex; ++i) {
		if (!(o << cont[i]))
			throw BadConversionError((o << "stringify(container[" << i << "])", o.str()));
		o << delimiter;
	}
	if (!(o << cont[maxIndex]))
		throw BadConversionError((o << "stringify(container[" << maxIndex << "])", o.str()));
	return o.str();
}

template<typename Container>
inline std::string stringify(const Container& cont, std::string delimiter, unsigned int offset)
{
	std::ostringstream o;
	if (cont.empty())
		return "";
	unsigned int maxIndex = cont.size() - 1;
	for (unsigned int i = 0; i < maxIndex; ++i) {
		if (!(o << (cont[i] + offset)))
			throw BadConversionError((o << "stringify(container[" << i << "])", o.str()));
		o << delimiter;
	}
	if (!(o << (cont[maxIndex] + offset)))
		throw BadConversionError((o << "stringify(container[" << maxIndex << "])", o.str()));
	return o.str();
}

template<>
inline std::string stringify(bool b)
{
	return b? "true" : "false";
}

class Str {
public:
	Str() {}
	template<class T> Str& operator << (const T& t) {
		m_oss << stringify(t);
		return *this;
	}
	Str& operator << (std::ostream& (*f) (std::ostream&)) {
		m_oss << f;
		return *this;
	}
	operator std::string() const {
		return m_oss.str();
	}
private:
	std::ostringstream m_oss;
};

template<typename T>
inline bool stringToValue(std::string const& str, T& value)
{
	std::istringstream istream(str);
	return !!(istream >> value);
}

template<>
inline bool stringToValue<bool>(std::string const& str, bool& value)
{
	std::istringstream istream(str);
	return !!(istream >> value);
}

template<typename T>
inline T parse(std::string const& str)
{
	std::istringstream istream(str);
	T value;
	if (!(istream >> value))
		throw BadConversionError(Str() << "Error converting '" << str << "' to " << TypeInfo<T>::type());
	return value;
}

// Template specialization for bool type to correctly parse "true" and "false"
template<>
inline bool parse<bool>(std::string const& str)
{
	std::istringstream istream(str);
	istream.setf(std::ios::boolalpha);
	bool value;
	if (!(istream >> value))
		throw BadConversionError(Str() << "Error converting '" << str << "' to bool");
	return value;
}

inline std::string firstWord(const std::string& line)
{
	std::istringstream ss;
	std::string buf;
	ss.str(line);
	ss >> buf;
	return buf;
}

inline void padString(std::string &str, const std::string::size_type newSize, const char paddingChar = ' ')
{
	if(newSize > str.size())
		str.append(newSize - str.size(), paddingChar);
}

template<typename T>
inline std::string padValue(T value, const std::string::size_type size, bool rightAligned = true, const char paddingChar = ' ')
{
	std::string valStr = stringify(value);
	if(size == valStr.size())
		return valStr;
	if (size < valStr.size())
		return valStr.substr(0, size);

	if (!rightAligned)
		return valStr.append(size - valStr.size(), paddingChar);

	return std::string(size - valStr.size(), paddingChar).append(valStr);
}

inline std::string toPrecision(double value, unsigned int precision = 10, bool fixed = false)
{
	std::ostringstream o;
	if (fixed)
		o << std::fixed << std::setprecision(precision);
	else
		o << std::setprecision(precision);
	if (!(o << value))
		throw BadConversionError((o << "stringify(" << value << ")", o.str()));
	return o.str();
}


inline std::string toPlural(std::string object, unsigned int num)
{
	if (num > 1 || num == 0)
		object.push_back('s');
	return object;
}

}

#ifdef NS_INFOMAP
}
#endif

#endif /* CONVERT_H_ */
