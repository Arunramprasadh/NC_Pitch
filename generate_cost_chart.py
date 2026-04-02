import matplotlib.pyplot as plt

# Data
labels = ['Namma Cloud Year 2', 'Namma Cloud Year 1', 'AWS / GCP']
values = [35, 55, 100]
colors = ['#1E4D7B', '#E8772E', '#64748B']  # Namma Blue, Namma Saffron, Slate

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 4))

# Create horizontal bars
bars = ax.barh(labels, values, color=colors, height=0.6)

# Customize axes and labels
ax.set_xlabel('TCO Index (%)', fontsize=12, fontweight='bold', color='#334155')
ax.set_title('Illustrative Cost Index Comparison', fontsize=14, fontweight='bold', color='#0D2137', pad=15)
ax.set_xlim(0, 110)

# Add data labels on the bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{int(width)}%', 
            ha='left', va='center', fontsize=11, fontweight='bold', color='#334155')

# Remove top and right spines for a clean look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
ax.spines['bottom'].set_color('#CBD5E1')

plt.tight_layout()

# Save the figure
plt.savefig('cost_comparison.png', dpi=300, bbox_inches='tight')
print("Saved cost_comparison.png")
