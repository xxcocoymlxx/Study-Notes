package ca.utoronto.utm.mcs;

public class Memory 
{
    private static long value = 0;

    public long getValue() {
        return value;
    }

    public void setValue(long newVal) {
        value = newVal;
    }

    public Memory() {}
}
