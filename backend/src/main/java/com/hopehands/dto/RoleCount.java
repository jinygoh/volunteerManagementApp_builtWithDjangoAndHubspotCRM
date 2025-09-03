package com.hopehands.dto;

public class RoleCount {
    private String preferredVolunteerRole;
    private long count;

    public RoleCount(String preferredVolunteerRole, long count) {
        this.preferredVolunteerRole = preferredVolunteerRole;
        this.count = count;
    }

    // Getters and Setters
    public String getPreferredVolunteerRole() {
        return preferredVolunteerRole;
    }

    public void setPreferredVolunteerRole(String preferredVolunteerRole) {
        this.preferredVolunteerRole = preferredVolunteerRole;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }
}
