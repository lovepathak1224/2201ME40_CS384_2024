def find_unique_triplets(nums):
  result = []
  n = len(nums)

  for i in range(n - 2):
    for j in range(i + 1, n - 1):
      for k in range(j + 1, n):
        if nums[i] + nums[j] + nums[k] == 0:
          triplet = sorted([nums[i], nums[j], nums[k]])
          if triplet not in result:
            result.append(triplet)

  return result


nums_str = input("Enter a list of integers separated by spaces: ")
nums = [int(x) for x in nums_str.split()]

triplets = find_unique_triplets(nums)
print(triplets)