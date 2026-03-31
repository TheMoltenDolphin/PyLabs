def can_pack(items, bins, item_idx, capacity):
    if item_idx == len(items):
        return True

    item = items[item_idx]
    for i in range(len(bins)):
        if bins[i] + item <= capacity:
            bins[i] += item
            if can_pack(items, bins, item_idx + 1, capacity):
                return True
            bins[i] -= item
        
        if bins[i] == 0:
            break
            
    return False

def solve_bin_packing(items, capacity):
    items.sort(reverse=True)
    
    for num_bins in range(1, len(items) + 1):
        bins = [0] * num_bins
        if can_pack(items, bins, 0, capacity):
            return num_bins, bins
    return None

item_sizes = [4, 8, 1, 4, 2, 1]
bin_capacity = 10

min_bins, final_state = solve_bin_packing(item_sizes, bin_capacity)

print(f"Minimum bins: {min_bins}")
print(f"Final filling: {final_state}")
