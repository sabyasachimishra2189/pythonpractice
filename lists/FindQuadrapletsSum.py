from collections import Counter


class Solution:

    def compare(self,totalList, searchableList):
        for i in totalList:
            if Counter(searchableList) == Counter(i):
                return True
            else:
                return False

    def fourSum(self, nums, target):
        result=[]
        if len(nums)<4:
            return
        nums.sort()
        totalL=len(nums)
        for i in range(len(nums)-3):

            for j in range(i+1,totalL-2):
                left=j+1
                right=totalL-1
                while left<right:
                    sum=nums[i]+nums[j]+nums[left]+nums[right]
                    if(sum==target):
                        combinations=[nums[i],nums[j],nums[left],nums[right]]
                        #combinations.sort()
                        if(self.compare(result,combinations) is not True):

                            result.append(combinations)
                        left=left+1
                        right=right-1
                    elif sum<target:
                        left=left+1
                    else:
                        right=right-1

        return result

    def fourSum2(self, nums, target):
        nums.sort()
        res = []
        #resnum = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                low, high = j + 1, len(nums) - 1
                while low < high:
                    #resnum += 1
                    tlist = [nums[i], nums[j], nums[low], nums[high]]
                    if sum(tlist) == target:
                        if tlist not in res:
                            res.append(tlist)
                        high -= 1
                        low += 1
                    elif sum(tlist) > target:
                        high -= 1
                    else:
                        low += 1

        #print(resnum)
        return res





s=Solution()
arr=[-3,-2,-1,0,0,1,2,3]
target=0
print(s.fourSum2(arr,target))