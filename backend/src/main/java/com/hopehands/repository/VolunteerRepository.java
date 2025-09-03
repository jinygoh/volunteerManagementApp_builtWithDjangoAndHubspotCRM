package com.hopehands.repository;

import com.hopehands.model.Volunteer;
import com.hopehands.dto.RoleCount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface VolunteerRepository extends JpaRepository<Volunteer, Long> {

    @Query("SELECT new com.hopehands.dto.RoleCount(v.preferredVolunteerRole, COUNT(v)) FROM Volunteer v GROUP BY v.preferredVolunteerRole ORDER BY COUNT(v) DESC")
    List<RoleCount> countByPreferredVolunteerRole();
}
