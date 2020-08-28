#ref leetcode
class Solution:

    def longestPalindrome(self, s: str) -> str:
        """
        :param s:
        :return:

        >>> solution = Solution()
        >>> solution.longestPalindrome('babad')
        'bab'
        >>> solution.longestPalindrome('cbbd')
        'bb'
        """
        res = ''
        t = '#'+'#'.join(s)+'#'
        for i, c in enumerate(t):
            left, right = i, i
            while 0 <= left-1 and right + 1 < len(t) and t[left-1] == t[right+1]:
                left = left - 1
                right = right + 1

            if len(t[left:right+1]) > len(res):
                res = t[left:right+1]

        return ''.join(res.split('#'))

if __name__ == '__main__':
    s=Solution()
    print(s.longestPalindrome("babad"))
