#include "string_utils.hpp"
#include <vector>
#include <string>
#include <boost/regex.hpp>


char** split_word(const char* word, size_t* size)
{
    *size = 0;
    std::string text_to_split(word);
    std::vector<std::string> splits;

    const size_t res = boost::regex_split(std::back_inserter(splits), text_to_split);

    const size_t length = splits.size();
    char** words = reinterpret_cast<char**>(malloc(sizeof(char*) * length));

    if (!words)
        return nullptr;

    for (size_t i = 0; i < length; ++i)
    {
        const size_t w_len = splits[i].length();
        char* word = reinterpret_cast<char*>(malloc(sizeof(char) * (w_len + 1)));

        if (!word) {
            for (size_t j = 0; j < i; ++j)
                free(words[i]);
            free(words);
            return nullptr;
        }

        std::memcpy(word, splits[i].data(), sizeof(char) * w_len);
        word[w_len] = '\x0';
        words[i] = std::move(word);
    }
    *size = length;

    return words;
}